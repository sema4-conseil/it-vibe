=
<template>
  <div class="container">
    <h1>About IT-Vibe</h1>
    <p>
      <strong>IT-Vibe</strong> is a public platform designed for IT
      professionals to share honest feedback about IT companies. Whether you are
      a current or former employee, IT-Vibe allows you to rate and review
      companies, providing valuable insights for future job seekers.
    </p>

    <h2>Key Features</h2>
    <ul>
      <li>Anonymous reviews to ensure open and honest feedback.</li>
      <li>
        Ratings on company culture, management, salary satisfaction, and
        work-life balance.
      </li>
      <li>Help future employees make informed career decisions.</li>
      <li>Gain insights into workplace trends and company reputations.</li>
      <li>
        Engage with a community of IT professionals sharing real experiences.
      </li>
    </ul>

    <h2>Why IT-Vibe?</h2>
    <p>
      Finding the right company in the IT industry can be challenging. IT-Vibe
      empowers job seekers with firsthand experiences and unbiased reviews,
      ensuring transparency in the workplace.
    </p>
  </div>
</template>

<script>
export default {
  name: "AboutPage",
};
</script>

<style scoped>
body,
html {
  margin: 0;
  padding: 0;
  height: 100%;
}

.container {
  display: flex; /* Use flexbox */
  flex-direction: column; /* Stack children vertically */
  min-height: 100vh;
  padding: 20px;
  box-sizing: border-box;
}

ul {
  list-style-type: none;
}
</style>
