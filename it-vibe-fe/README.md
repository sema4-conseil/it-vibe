# it-vibe-fe

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Compiles and minifies for production
```
npm run build
```

### Create docker image on nginx
```
docker build -t it-vibe-static-site .
```

### Run docker image locally
```
docker run --name it-vibe -d -p 8080:80 it-vibe-static-site
```

### Deploy on s3 with terraform
```
terraform apply
```


### Destroy terraform resources
```
terraform destroy
```
