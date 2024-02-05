# Harvesting NUSL

We have an offline harvest stored inside the CESNET CEPH,
which is accessible via S3 protocol.

To run the harvest:

0. Start the repo in development mode to make sure everything is running
   and import fixtures to the database.
1. Ask @tomash for read access to tenant 83e4e229*ef0205
2. Create the following files:

~/.aws/config
```
[profile nrdocs-dump]
endpoint_url = https://s3.cl4.du.cesnet.cz
```

~/.aws/credentials
```
[nrdocs-dump]
aws_access_key_id = <your-access-key>
aws_secret_access_key = <your-secret-key>
```

3. Run the following command:

```bash
./scripts/import_data.sh
```
This will create an offline harvester pre-configured 
with bucket and harvest name and will run the harvest.

The harvest takes data completely from s3, nusl is not
contacted.
