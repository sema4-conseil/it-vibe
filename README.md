# It-Vibe

## Overview

`it-vibe` is a project developed and maintained by _SEMA4 Conseil_. This project aims to provide a comprehensive solution for IT workers, such as developers, business analysts, scrum masters, and product owners, to review ESN (Entreprise de Services du Numérique) companies in France.

### Components

#### Front-end

- (dev) : http://it-vibe.dev.sema4-conseil.com/
- (prod) : http://it-vibe.sema4-conseil.com/

##### Technologies

- VueJS

##### Run locally

```
npm run serve
```

##### Build for staggig

```
npm run build -- --mode stg
```

#### Back-end

##### API

|             | DEV                                                   | PROD                                                  |
| ----------- | ----------------------------------------------------- | ----------------------------------------------------- |
| Healthcheck | https://dev.api.it-vibe.sema4-conseil.com/healthcheck | https://dev.api.it-vibe.sema4-conseil.com/healthcheck |
