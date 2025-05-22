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
          placeholder="Write your message..."
          minlength="25"
          rows="5"
          required
          class="form-control"
        ></textarea>
        <div
          v-if="contactMessage.content"
          :class="
            contactMessage.content.length < 25 ? 'text-red' : 'text-green'
          "
        >
          <span
            >Current message length: {{ contactMessage.content.length }}</span
          >
        </div>
      </div>
      <button type="submit" class="contact-button">Send</button>
    </form>
  </div>
</template>

<script>
export default {
  constants: {
    MIN_MESSAGE_LENGTH: 25,
  },
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

    validateForm() {
      let validationErrors = [];
      // Validate email format
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(this.contactMessage.email)) {
        validationErrors.push("Please enter a valid email address.");
      }
      // Validate message length
      if (this.contactMessage.content.length < this.MIN_MESSAGE_LENGTH) {
        validationErrors.push(
          "Message must be at least " +
            this.MIN_MESSAGE_LENGTH +
            " characters long."
        );
      }
      return validationErrors;
    },
    async handleSubmit() {
      let validationErrors = this.validateForm();
      if (validationErrors.length > 0) {
        alert(validationErrors.join("\n"));
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
