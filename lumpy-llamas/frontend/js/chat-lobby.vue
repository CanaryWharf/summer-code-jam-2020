<template>
<div v-if="ready">
  <div>
    <fieldset>
    <legend>Go chat with some random people!</legend>
        <div class="form-group">
          <label for="text">Chatroom Name</label>
          <input v-model="roomName" id="text" name="itext" type="text" 
            placeholder="(Alphanumeric and 1 and 20 characters long)" 
            minlength="1" maxlength="20">
          <div>
            <input v-model="makePrivateChat" type="checkbox" id="private" name="private" value="">
            <label for="private"> Make this a private chat room?</label>
          </div>
          <div v-if="makePrivateChat">
            <button v-on:click="getUsers" class="btn btn-default">Refresh user list</button><br>
            <label for="permitted-users">Please select at least 2 permitted users:</label>
            <div class="selected-users">
              <multiselect v-model="selected" :options="options" :multiple="true" :close-on-select="false" :clear-on-select="false" 
                :preserve-search="true" placeholder="Select your users" label="user" track-by="user">
                <template slot="selection" slot-scope="{ values, search, isOpen }"><span class="multiselect__single" 
                  v-if="values.length &amp;&amp; !isOpen">{{ values.length }} options selected</span></template>
              </multiselect>
            </div>
          </div>
        </div>
        <button v-on:click="goToChatRoom" class="btn btn-default">Enter Chatroom</button>
        <p>{{ message }}</p>
    </fieldset>
  </div>
</div>
</template>

<style>
::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
  color: pink;
  opacity: 1; /* Firefox */
}
.select-users {
  width: 100%;
  border: 0.1em solid green;
  padding: 0.5em;
  margin: 1em;
}
</style>

<script>
import axios from 'axios';
import Multiselect from 'vue-multiselect';

export default {
  components: {Multiselect},
  data() {
    return {
        roomName: '',
        ready: true,
        message: null,
        makePrivateChat: false,
        options: [],
        selected: [],
    }
  },
  beforeMount() {
    this.getUsers()
  },
  methods: { 
    goToChatRoom() {
        var selected_usernames= this.selected.map(x => x.user)

        var payload = {
            roomName: this.roomName,
            private: this.makePrivateChat,
            users: selected_usernames,
          }

        console.log(payload)

        axios.post('/api/chat/gotoroom/', payload).then((response) => {
            if (response.data.valid) {
                this.message = null;
                window.location.pathname = '/chat/room/' + this.roomName + '/';
            }
            else {
                this.message = response.data.message
            }
        }, (error) => {
            console.log(error);
        })    
    },
    getUsers() {
      axios.get('/api/chat/users/').then((response) => {
            this.options = response.data.users
        }, (error) => {
            console.log(error);
        })
    }
  }
}
</script>
