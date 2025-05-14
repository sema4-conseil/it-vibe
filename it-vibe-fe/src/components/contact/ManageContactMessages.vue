<template>
  <div>
    <div class="search-container">
      <input
        type="radio"
        id="new"
        value="NEW"
        v-model="loadedStatus"
        @change="changeStatus"
      />
      <label for="new"><span class="status-badge status-1">New</span></label>
      <input
        type="radio"
        id="in-progress"
        value="IN_PROGRESS"
        v-model="loadedStatus"
        @change="changeStatus"
      />
      <label for="in-progress"
        ><span class="status-badge status-2">In Progress</span></label
      >
      <input
        type="radio"
        id="done"
        value="DONE"
        v-model="loadedStatus"
        @change="changeStatus"
      />
      <label for="done"><span class="status-badge status-3">Done</span></label>
      <input
        type="radio"
        id="archived"
        value="ARCHIVED"
        v-model="loadedStatus"
        @change="changeStatus"
      />
      <label for="archived"
        ><span class="status-badge status-4">Archived</span></label
      >
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
          <tr
            v-for="message in messages"
            :key="message.id"
            @click="this.selectedMessage = message"
          >
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
                v-if="message.status != 4"
                v-model="message.status"
                @change="this.updateStatus(message)"
                :disabled="message.status == 4"
              >
                <option
                  v-for="status in transitions[message.status]"
                  :key="status"
                  :value="status"
                >
                  {{ this.status[status] }}
                </option>
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
    <div class="message-container" v-if="selectedMessage">
      <p>
        <strong>From: </strong>
        <span class="email-address">{{ selectedMessage.email }}</span>
      </p>
      <p>
        <strong>Status: </strong
        ><span :class="'status-badge status-' + selectedMessage.status">
          {{ this.status[selectedMessage.status] }}
        </span>
      </p>
      <p><strong>Content:</strong> {{ selectedMessage.content }}</p>
      <button @click="selectedMessage = null">Close</button>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      selectedMessage: null,
      loadedStatus: "NEW",
      status: {
        1: "New",
        2: "In Progress",
        3: "Done",
        4: "Archived",
      },
      transitions: {
        1: [2, 4],
        2: [3],
        3: [4],
        4: [],
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
      this.selectedMessage = null;
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
    async changeStatus() {
      this.lastEvaluatedKey = null;
      this.messages = [];
      this.selectedMessage = null;
      this.loading = true;
      await this.fetchMessages();
    },
    updateStatus(message) {
      let codes = {
        1: "NEW",
        2: "IN_PROGRESS",
        3: "DONE",
        4: "ARCHIVED",
      };
      let status = codes[message.status];
      let url = `${this.apibaseUrl}/contact/${message.id}`;
      const token = sessionStorage.getItem("idToken");
      let body = {
        status: status,
      };
      fetch(url, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      })
        .then((response) => {
          if (!response.ok) {
            alert("Failed to update status");
          }
        })
        .catch((error) => {
          console.error("Error updating status", error);
        })
        .finally(() => {
          this.selectedMessage = null;
          this.lastEvaluatedKey = null;
          this.messages = [];
          this.loading = true;
          this.fetchMessages();
        });
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

.message-container {
  margin: 20px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  background-color: white;
  text-align: left;
}
</style>
