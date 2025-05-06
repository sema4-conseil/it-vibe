<template>
  <div class="container">
    <h1>Contact Us</h1>
    <form @submit.prevent="handleSubmit" class="contact-form">
      <div class="form-group">
        <label for="email">Email Address:</label>
        <input
          type="email"
          id="email"
          v-model="contactMessage.email"
          placeholder="Enter your email"
          required
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label for="message">Message:</label>
        <textarea
          id="message"
          v-model="contactMessage.content"
          placeholder="Enter your message, it should be at least 10 characters long"
          minlength="10"
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
      apibaseUrl: process.env.VUE_APP_API_BASE_URL,
      contactMessage: {
        email: "",
        message: "",
      },
    };
  },
  methods: {
    resetForm() {
      this.contactMessage.email = "";
      this.contactMessage.content = "";
    },
    async handleSubmit() {
      // Validate email format
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(this.contactMessage.email)) {
        alert("Please enter a valid email address.");
        return;
      }

      // Validate message length
      if (this.contactMessage.content.length < 100) {
        alert("Message must be at least 100 characters long.");
        return;
      }
      try {
        const response = await fetch(`${this.apibaseUrl}/contact`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.contactMessage),
        });
        if (!response.ok) {
          throw new Error("Failed to create company");
        }
        let data = await response.json();
        alert(data.message);
        this.resetForm();
      } catch (error) {
        alert("An error occurred while submitting your review.");
      }
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
