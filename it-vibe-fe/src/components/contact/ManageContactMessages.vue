<template>
  <div>
    <div class="search-container">
      <input
        type="radio"
        id="new"
        value="NEW"
        v-model="loadedStatus"
        @change="fetchMessages"
      />
      <label for="new"><span class="status-badge status-1">New</span></label>
      <input
        type="radio"
        id="in-progress"
        value="IN_PROGRESS"
        v-model="loadedStatus"
        @change="fetchMessages"
      />
      <label for="in-progress"
        ><span class="status-badge status-2">In Progress</span></label
      >
      <input
        type="radio"
        id="done"
        value="DONE"
        v-model="loadedStatus"
        @change="fetchMessages"
      />
      <label for="done"><span class="status-badge status-3">Done</span></label>
    </div>
    <div v-if="loading">
      <p>Loading contact messages ...</p>
      <div class="spinner"></div>
    </div>

    <div v-else-if="messages" class="table-container">
      <table>
        <thead>
          <tr>
            <th>Recieved on</th>
            <th>Email</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="message in messages" :key="message.id">
            <!-- Convert timestamp to local dateTime -->
            <td>{{ this.formatLocalDateTime(message.timestamp) }}</td>
            <td>
              <span class="email-address">{{ message.email }}</span>
            </td>
            <td>
              <span :class="'status-badge status-' + message.status">
                {{ this.status[message.status] }}
              </span>
            </td>
            <td>
              <select
                v-model="message.status"
                @change="updateStatus(message)"
                :disabled="message.status == 3 || message.status == 4"
              >
                <option value="1">New</option>
                <option value="2">In Progress</option>
                <option value="3">Done</option>
              </select>
            </td>
          </tr>
        </tbody>
      </table>
      <div>
        <span>Loaded : {{ messages.length }} messages</span>
      </div>
      <button @click="fetchMessages()" :disabled="!this.lastEvaluatedKey">
        <i class="fa fa-forward"></i>Next Items
      </button>
    </div>
  </div>
</template>
<script>
// eslint-disable-next-line
import { copyToClipboard } from "@/utils/copyToClipboard";

export default {
  data() {
    return {
      loadedStatus: "NEW",
      status: {
        1: "New",
        2: "In Progress",
        3: "Done",
        4: "Archived",
      },
      messages: [],
      lastEvaluatedKey: null,
      pageSize: 10,
      loading: false,
      apibaseUrl: process.env.VUE_APP_API_BASE_URL,
    };
  },
  mounted() {
    this.fetchMessages();
  },
  methods: {
    async fetchMessages() {
      const token = sessionStorage.getItem("idToken");
      let url = `${this.apibaseUrl}/contact?pageSize=${this.pageSize}`;
      if (this.lastEvaluatedKey) {
        url += `&startKey=${encodeURIComponent(
          JSON.stringify(this.lastEvaluatedKey)
        )}`;
      }
      url += "&status=" + this.loadedStatus;
      try {
        this.loading = true;
        const response = await fetch(url, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
        const data = await response.json();
        this.messages = data.items;
        this.lastEvaluatedKey = data.lastEvaluatedKey;
        this.loading = false;
      } catch (error) {
        this.loading = false;
      }
    },
    formatLocalDateTime(epoch) {
      if (!epoch) return "";

      // Convert epoch seconds to milliseconds (JavaScript uses ms)
      const date = new Date(epoch * 1000);

      const options = {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
      };

      return date.toLocaleString(undefined, options);
    },
    changeStatus(status) {
      this.loadedStatus = status;
      this.fetchMessages();
    },
  },
};
</script>
<style scoped>
.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8em;
  font-weight: 500;
}

.status-1 {
  /* New */
  background-color: var(--light-red);
  color: var(--dark-red);
}

.status-2 {
  /* In Progress */
  background-color: #fff3cd;
  color: #856404;
}

.status-3 {
  /* Resolved */
  background-color: #d4edda;
  color: #155724;
}

.status-4 {
  /* Archived */
  background-color: #e2e3e5;
  color: #383d41;
}
</style>
