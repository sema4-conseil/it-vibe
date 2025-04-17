<template>
  <div>
    <button @click="redirectToCognitoLogin">Go to login page</button>
  </div>
</template>

<script>
export default {
  methods: {
    redirectToCognitoLogin() {
      const cognitoConfig = {
        clientId: process.env.VUE_APP_COGNITO_USER_POOL_CLIENT_ID,
        userPoolDomain: process.env.VUE_APP_COGNITO_USER_POOL_DOMAIN,
        redirectUri: process.env.VUE_APP_LOGIN_REDIRECT_URI,
      };

      const loginUrl = `https://${
        cognitoConfig.userPoolDomain
      }/login?client_id=${
        cognitoConfig.clientId
      }&response_type=code&redirect_uri=${encodeURIComponent(
        cognitoConfig.redirectUri
      )}`;
      window.location.href = loginUrl;
    },
  },
};
</script>
