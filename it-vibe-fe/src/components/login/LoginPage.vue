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
        defaultRedirectUri: process.env.VUE_APP_LOGIN_REDIRECT_URI,
      };
      const redirectUri = this.$route.query.redirect_uri;

      if (redirectUri)
        // store it in session storage
        sessionStorage.setItem("redirect_uri", redirectUri);

      const loginUrl = `https://${
        cognitoConfig.userPoolDomain
      }/login?client_id=${
        cognitoConfig.clientId
      }&response_type=code&redirect_uri=${encodeURIComponent(
        cognitoConfig.defaultRedirectUri
      )}`;
      window.location.href = loginUrl;
    },
  },
};
</script>
