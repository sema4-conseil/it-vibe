<template>
  <div>
    <p>Processing login...</p>
  </div>
</template>

<script>
export default {
  mounted() {
    console.log("CallBack component mounted");
    this.handleCognitoCallback();
  },
  methods: {
    async handleCognitoCallback() {
      const url = new URL(window.location.href);
      const code = url.searchParams.get("code");
      if (code) {
        const cognitoConfig = {
          clientId: process.env.VUE_APP_COGNITO_USER_POOL_CLIENT_ID,
          userPoolDomain: process.env.VUE_APP_COGNITO_USER_POOL_DOMAIN,
          redirectUri: process.env.VUE_APP_LOGIN_REDIRECT_URI,
        };

        const tokenUrl = `https://${cognitoConfig.userPoolDomain}/oauth2/token`;
        const bodyData = new URLSearchParams({
          grant_type: "authorization_code",
          client_id: cognitoConfig.clientId,
          code: code,
          redirect_uri: cognitoConfig.redirectUri,
        });

        try {
          const response = await fetch(tokenUrl, {
            method: "POST",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
            body: bodyData.toString(),
          });

          if (response.ok) {
            const tokens = await response.json();
            sessionStorage.setItem("accessToken", tokens.access_token);
            sessionStorage.setItem("idToken", tokens.id_token);
            sessionStorage.setItem("refreshToken", tokens.refresh_token);
            window.location.href = "/"; // Redirect to home or another page
          } else {
            console.error(
              "Failed to exchange code for tokens:",
              await response.text()
            );
          }
        } catch (error) {
          console.error("Error during token exchange:", error);
        }
      }
    },
  },
};
</script>
