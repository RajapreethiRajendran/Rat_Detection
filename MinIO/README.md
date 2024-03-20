# Minio Deployment features
The MinIo database has been created via the Deployment artifact. 
The use of persistant  volume is important to ensure that the data and 
the images in the buckets will not be lost in case of the restart 
or the crash of the pods. The service has also been added in order 
to make the command line and UI from MinIO accessible over the network 
externally to support testing and integration activities 
