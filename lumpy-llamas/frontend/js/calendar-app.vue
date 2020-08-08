<template>

  <div v-if="ready"> # this tells the page to not render until the page is ready
      # access objects directly with {{ myStuff.heading }} is the JS equivalent of {{ myStuff['heading'] }}
    <h2 class="some-heading">Hello and welcome to {{ myStuff.heading }}</h2>
    <main id="calendar">
      <div>S</div>
      <div>M</div>
      <div>T</div>
      <div>W</div>
      <div>T</div>
      <div>F</div>
      <div>S</div> 
      <div v-for="(day, index) in days" :style="{ gridColumn: column(index) }" :class="{ today: today(day) }">
        {{ day.format('D') }}
    </div>
    </main>
    <ul>
      <li v-for="item in myStuff" :key="item">
        My item name is: {{item}}
      </li>
    </ul>
    # Links can be done like this
    <router-link :to="{ name: 'some_page_name' }">Click Here</router-link>
  </div>
</template>

<style>
.some-heading {
  font-size: xx-large;
  color: pink;
}
</style>

<script>

import axios from 'axios';

export default {
  data() {
    return {
      myStuff: null,
      ready: false,
    };
  },
  beforeMount() {
    this.getData();
  },
  methods: {
    getData() {
      axios.get('/api/calendarapp/current').then((response) => {
        this.myStuff = response.data;
        this.ready = true;
      });
    },
  },
};

const app = new Vue({
  el: '#calendar',
  data() {
    return {
      days: []  
    };
  }, 
  methods: {
    column(index) {
      if (index == 0) {
        return this.days[0].day() + 1
      };
    },
    today(day) {
      return moment().isSame(day, 'day')
    },
  },
  mounted() {
    let monthDate = moment().startOf('month')
    
    this.days = [...Array(monthDate.daysInMonth())].map((_, i) => monthDate.clone().add(i, 'day'))
  },
});
</script>
