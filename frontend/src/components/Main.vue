<template>
  <div class="main">
    <Row style="margin-top:20px;">
      <Col span="2" offset="5">
        <h1>任务列表</h1>
      </Col>
      <Col span="2" offset="18">
        <Button type="primary" shape="circle" icon="md-add" @click="newTask">新建任务</Button>
      </Col>
    </Row>
    <Row style="margin-top:10px;">
      <Col span="15" offset="5">
        <Card :bordered="false" style="margin:5px;">
          <Row>
            <Col span="4">任务id</Col>
            <Col span="10">任务实例id</Col>
            <Col span="5">任务状态</Col>
            <Col span="5">任务创建时间</Col>
          </Row>
        </Card>
        <Card v-for="(task, index) in tasklist" :bordered="false" style="margin:5px;" v-on:click.native="getTask">
          <Row>
            <Col span="4">{{ task.id }}</Col>
            <Col span="10">{{ task.instance }}</Col>
            <Col span="5">{{ task.state }}</Col>
            <Col span="5">{{ task.create_time }}</Col>
          </Row>
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script>
export default {
  name: 'Main',
  data () {
    return {
      tasklist: []
    }
  },
  mounted () {
    this.getTaskList()
  },
  methods: {
    getTaskList() {
      this.$http.get("/api/task").then(res => {
        for (var i = 0; i < res.data.data.length; i++) {
          this.tasklist.push(res.data.data[i])
        }
      }).catch(err => {
        console.log(err)
      })
    },
    newTask () {
      console.log("new task")
      /*this.$http.post("/api/task").then(res => {
        //
      }).catch(err => {
        console.log(err)
      })*/
    },
    getTask () {
      console.log("get task")
      /*this.$http.post("/api/task").then(res => {
        //
      }).catch(err => {
        console.log(err)
      })*/
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.main {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 60px;
  background-color: #eee;
}
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
