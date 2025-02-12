<template>
  <div class="container">
    <h1>Contact Us</h1>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="email">Email Address:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="message">Message:</label>
        <textarea
          id="message"
          v-model="message"
          minlength="100"
          required
        ></textarea>
      </div>
      <button type="submit">Send</button>
    </form>
  </div>
</template>
<script>
export default {
  name: "ContactPage",
};
</script>
<style scoped>
.contact-page {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: none;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.contact-page h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-group textarea {
  resize: vertical;
  min-height: 150px;
}

button[type="submit"] {
  display: block;
  width: 50%;
  padding: 10px;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: rgb(122, 122, 122);
}

.container {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: left;
}
</style>
