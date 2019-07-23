<template>
  <div id="app">
    <Menu mode="horizontal" theme="dark" active-name="1">
      <MenuItem name="home" on-select="gohome">
        <Icon type="ios-home" />
        首页
      </MenuItem>
    </Menu>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  methods: {
    gohome () {
      router.push('/')
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
