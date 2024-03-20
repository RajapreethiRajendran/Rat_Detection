import React, { useEffect, useState } from "react";
import "./styles.css";
import * as minio from "minio";

export default function App() {
  const [buckets, setBuckets] = useState([]);

  useEffect(() => {
    const getBuckets = async () => {
      // create the client
      const mc = new minio.Client({
        endPoint: "play.min.io",
        port: 9000,
        useSSL: true,
        accessKey: "Q3AM3UQ867SPQQA43P2F",
        secretKey: "zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG"
      });
      // list buckets
      const res = await mc.listBuckets();

          // Check if Bucket Exists 
          mc.bucketExists('cloudcomputing', function(err, exists) {
            if (err) {
              return console.log(err)
            }
            if (exists) {
              
            // } else { // Create a bucket called cloudcomputing.
            //   mc.makeBucket('cloudcomputing', 'us-east-1', function(err) {
            //     if (err) {
            //       return console.log(err)
            //     }
            //     console.log('Bucket created successfully in "us-east-1".')
            //   }
    
        // File that needs to be uploaded.
        var file = '/Users/prasanna/Documents/College/3rd_Sem/Cloud Computing/minio-UI/Upload.jpeg'
        console.log("Upload File path :", file)
          
        var metaData = {
          'Content-Type': 'application/octet-stream',
          'X-Amz-Meta-Testing': 1234,
          'example': 5678
      }
    
      // Using putObject API upload your file to the bucket cloudcomptuing.
      mc.putObject('cloudcomputing', 'Upload.jpeg', file, metaData, function(err, etag) {
        if (err) return console.log(err)
        console.log('File uploaded successfully.')
      }); 
      return console.log('Bucket exists.')  
      }
      });
    
      // List all object paths in bucket cloudcomputing.
        var objectsStream = mc.listObjects('cloudcomputing', '', true)
        objectsStream.on('data', function(obj) {
          console.log(obj)
        })
        objectsStream.on('error', function(e) {
          console.log(e)
        })

      setBuckets(res);
    };
    getBuckets();
  }, []);

  return (
    <div className="App">
      <h1>Minio example</h1>

      <ul>
        {buckets.slice(0, 5).map((bucket, index) => (
          <li key={index}>{bucket.name}</li>
        ))}
      </ul>
    </div>
  );
}
