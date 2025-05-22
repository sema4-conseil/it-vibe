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
    <generic-modal
      v-if="this.modal.show"
      :isOpen="this.modal.show"
      @close="modal.show = false"
    >
      <div>
        <h3>Info</h3>
        <p>{{ this.modal.message }}</p>
        <div v-if="this.modal.loading" class="spinner"></div>
      </div>
    </generic-modal>
  </div>
</template>

<script>
import GenericModal from "@/components/ui/GenericModal.vue";
export default {
  components: { GenericModal },
  constants: {
    MIN_MESSAGE_LENGTH: 25,
  },
  name: "ContactPage",
  data() {
    return {
      modal: {
        show: false,
        message: "",
        type: "",
        loading: false,
      },
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
        this.modal.message = validationErrors.join("\n");
        this.modal.show = true;
        return;
      }
      try {
        this.modal.loading = true;
        this.modal.message = "Sending message...";
        this.modal.show = true;
        const response = await fetch(`${this.apibaseUrl}/contact`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.contactMessage),
        });
        if (!response.ok) {
          throw new Error("Problem sending message");
        }
        this.modal.message =
          "Thank you for your message! We will get back to you soon.";
        this.modal.loading = false;
        this.resetForm();
      } catch (error) {
        this.modal.message =
          "An error occurred while sending your message. Please try again.";
        this.showModal = true;
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
