#!/usr/bin/python3
import os
import socket
import sys
import mimetypes
import urllib
from typing import List
from contextlib import contextmanager

class __Nav:
    PORT=8080

    def __init__(self):
        self.outFile=None # le fichier utilisable pour dialoguer avec le navigateur
        self.form={} # le dictionnaire contenant les variables du formulaire
        self.path="" # le chemin de l'URL
        self.method="" # la méthode de la requête (GET ou POST)
        self._allowedDownloads=[] # les fichiers à servir directement
        self._verbose=True
        self._debug=False
        self.ignorePath=["/favicon.ico"]
        
    def verbose(self,boolean):
        """
        active ou désactive l'affichage des messages du nano-serveur
        """
        self._verbose=boolean

    def debug(self,boolean):
        """
        active ou désactive le mode debug
        """
        self._debug=boolean
        
    def allowDL(self,list:List[str]):
        """
        indique quelle est la liste de fichiers (dans le répértoire courant) qui peuvent être servis directement par le nano-serveur. La liste doit contenir des noms de fichiers, sans chemin. Chaque nouvel appel remplace la liste précédente.
        """
        self._allowedDownloads=list

    def beginPage(self):
        """
        Cette méthode attend que le navigateur demande une page.

        Elle analyse la requête du client et met à jour les variables path, method et form (un dictionnaire avec les variables d'un éventuel formulaire).

        Après l'appel à cette méthode, le programme doit utiliser la méthode write() ou la méthode print() pour envoyer du code HTML au navigateur.
                
        Quand tout le code a été envoyé au navigateur, le programme doit appeler la méthode endPage().
        """
        self.path=""
        self.form={}
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("localhost",self.PORT))
        self.sock.listen(1)
        # il y a une boucle pour ignorer les connections non pertinentes ou gérer les fichiers, mais en réalité, on ne gère qu'une connection
        while True: 
            self.conn, addr = self.sock.accept()
            self.inFile=self.conn.makefile("r")
            self.outFile=self.conn.makefile("w")
            # read server request
            line=self.inFile.readline()
            tokens=line.split()
            if len(tokens)<3:
                if self._verbose:
                    print("Connexion non HTTP depuis",addr,file=sys.stderr)
                self.close()
                continue
            self.method=tokens[0]
            self.path=tokens[1]
            contentLength=-1
            if self._debug:
                print(line,end="",file=sys.stderr)
            # read HTTP header
            while True:
                line=self.inFile.readline()
                if self._debug:
                    print(line,end="",file=sys.stderr)
                    #print(len(line),":",line.encode().hex(),file=sys.stderr)
                # ??? vérifier si readline met un \n ?
                if line=="\n" or line=="" or line=="\r" or line=="\r\n":
                    break
                if line.startswith("Content-Length:"):
                    contentLength=int(line.split()[1])

            if self.method=="POST":
                data=self.inFile.read(contentLength)
                if self._debug:
                    print(data,file=sys.stderr)
                tokens=data.split("&")
                for t in tokens:
                    words=t.split("=")
                    self.form[urllib.parse.unquote_plus(words[0])]=urllib.parse.unquote_plus(words[1])
            elif self.method=="GET":
                query=urllib.parse.urlparse(self.path)
                if self._debug:
                    print(query,file=sys.stderr)
                self.path=query.path
                list=urllib.parse.parse_qsl(query.query,keep_blank_values=True)
                for key,val in list:
                    self.form[key]=val
            else:
                self.outFile.write("HTTP/1.1 405 Method Not Allowed\r\n")
                self.outFile.write("Content-Type: text/html; charset=utf-8\r\n")
                self.outFile.write("Connection: close\r\n")
                self.outFile.write("\r\n")
                self.outFile.write("La méthode "+self.method+" n'est pas gérée.")
                self.close()
                continue

            if self.path in self.ignorePath:
                # ignore the request
                self.outFile.write("HTTP/1.1 404 Not Found\r\n")
                self.outFile.write("Content-Type: text/html; charset=utf-8\r\n")
                self.outFile.write("Connection: close\r\n")
                self.outFile.write("\r\n")
                self.close()
                continue
            
            # envoi de fichiers autorisés
            if len(self.path)>1 and self.path[0]=="/" and self.path[1:] in self._allowedDownloads:
                self._serveFile(self.path[1:])
                continue

            # on a une page à générer, on sort de la boucle
            break

        # send client answer
        self.outFile.write("HTTP/1.1 200 OK\r\n")
        self.outFile.write("Content-Type: text/html; charset=utf-8\r\n")
        self.outFile.write("Cache-Control: no-cache, no-store, must-revalidate\r\n")
        self.outFile.write("Connection: close\r\n")
        self.outFile.write("\r\n")
    
    def endPage(self):
        """
        doit être appelé pour indiquer que la page HTML a été complètement générée.
        """
        self.close()

    def close(self):
        self.inFile.close()
        self.outFile.close()
        self.conn.close()
        
    def write(self,str):
        self.outFile.write(str)

    def print(self,*a,**b):
        old=sys.stdout
        sys.stdout=self.outFile
        print(*a,**b)
        sys.stdout=old
        
    def _serveFile(self,filename):
        (mimetype,encoding)=mimetypes.guess_type(filename)
        if not os.path.exists(filename):
            if self._verbose:
                print("Demande du fichier '",filename,"' dont le téléchargement est autorisé mais qui n'existe pas.",sep="",file=sys.stderr)
            self.outFile.write("HTTP/1.1 404 Not Found\r\n")
            self.outFile.write("Content-Type: text/html; charset=utf-8\r\n")
            self.outFile.write("Connection: close\r\n")
            self.outFile.write("\r\n")
            self.outFile.write("Le fichier demandé ("+filename+") est autorisé au téléchargement mais n'existe pas.")
            self.close()
        else:
            if self._verbose:
                print("Envoi du fichier '",filename,"' dont le téléchargement est autorisé",sep="",file=sys.stderr)
            self.outFile.write("HTTP/1.1 200 OK\r\n")
            if mimetype==None:
                mimetype="application/octet-stream"
            self.outFile.write("Content-Type: "+mimetype+"\r\n")
            self.outFile.write("Connection: close\r\n")
            self.outFile.write("\r\n")
            self.outFile.flush()
    
            with open(filename, "rb") as f:
                while True:
                    data=f.read(4096)
                    if not data:
                        break
                    self.conn.sendall(data)
            self.close()

nav=__Nav()

# à utiliser avec with redirectStdout(file): ...
@contextmanager
def redirectStdout(fileobj):
    old = sys.stdout
    sys.stdout = fileobj
    try:
        yield fileobj
    finally:
        sys.stdout = old

        
