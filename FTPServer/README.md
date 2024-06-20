# 🛠️ FTP Server Setup  

We will be using Pyftpdlib (Python FTP server) to set our FTP Server.  

---  

## 🐍🛠️ Pyftpdlib Setup  

* Change your directory to '__File__' to save the received file from the client

```
# change dir to 'File'
cd File
```  

* To install python's __pyftpdlib__ module  

```
# to install the module 
pip install pyftpdlib

```  

## 🗄️ Run the Server  

```
# To start the FTP Server  
python3 -m pyftpdlib -w --user=your_username --password=your_password
```  


## 📝 Note:  

If your __client__ is __Unix/Linux__ based. Run "__rename.sh__" to rename the file(s) of the __File__ directory because the received file get saved as "__.filename.log__" in Linux it is consider to be a hidden file.  

```
# to make it executable
chmod +x rename.sh

# to run
./rename.sh
```  



