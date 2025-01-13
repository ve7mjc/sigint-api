## Misc Scratch Notes

Assuming minio profile is `minio` from herein.

- Add bucket read-write policy: `mc admin policy create minio intercept-api_readwrite intercept-api_readwrite-policy.json`

- List Buckets: `mc ls minio`
- List Users: `mc admin user list minio`
- List Accesskeys: `mc admin accesskey list minio`
- Add user: `mc admin user add myminio <access-key> <secret-key>`

- List policies: `mc admin policy list minio`
- View specific policy: `mc admin policy info minio readwrite` (readwrite is name of policy here)
- View attached policies of user: `mc admin user info minio intercept-api` (user = intercept-api)

mc admin policy create TARGET POLICYNAME POLICYFILE

- Upload policy: `mc admin policy create minio readwrite readwrite-policy.json`

- Attach Policy: mc admin policy attach minio readwrite --user intercept-api

