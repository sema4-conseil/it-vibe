<template>
  <div>
    <button @click="logout">Sure you want to logout ?</button>
  </div>
</template>

<script>
export default {
  methods: {
    logout() {
      // Cognito configuration
      const cognitoConfig = {
        clientId: process.env.VUE_APP_COGNITO_USER_POOL_CLIENT_ID,
        userPoolDomain: process.env.VUE_APP_COGNITO_USER_POOL_DOMAIN,
        redirectUri: process.env.VUE_APP_LOGIN_REDIRECT_URI,
        postLogoutRedirectUri: process.env.VUE_APP_LOGOUT_REDIRECT_URI,
      };

      // Clear tokens from sessionStorage
      sessionStorage.removeItem("accessToken");
      sessionStorage.removeItem("idToken");
      sessionStorage.removeItem("refreshToken");

      // Redirect to Cognito logout endpoint
      const logoutUrl = `https://${
        cognitoConfig.userPoolDomain
      }/logout?client_id=${
        cognitoConfig.clientId
      }&logout_uri=${encodeURIComponent(cognitoConfig.postLogoutRedirectUri)}`;
      window.location.href = logoutUrl;
    },
  },
};
</script>
