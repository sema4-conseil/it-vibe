<template>
  <div class="container">
    <h1>Contact Us</h1>
    <form @submit.prevent="handleSubmit" class="contact-form">
      <div class="form-group">
        <label for="email">Email Address:</label>
        <input
          type="email"
          id="email"
          v-model="email"
          required
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label for="message">Message:</label>
        <textarea
          id="message"
          v-model="message"
          minlength="100"
          required
          class="form-control"
        ></textarea>
      </div>
      <button type="submit" class="contact-button">Send</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "ContactPage",
  data() {
    return {
      email: "",
      message: "",
    };
  },
  methods: {
    handleSubmit() {
      // Handle form submission logic here
      console.log("Email:", this.email);
      console.log("Message:", this.message);
      // You can add your API call or other submission logic here
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  border-radius: 8px;
}

textarea.form-control {
  resize: vertical; /* Allow vertical resizing */
  min-height: 150px;
}

.contact-button {
  align-self: flex-start; /* Align button to the start of the flex container */
}
</style>
