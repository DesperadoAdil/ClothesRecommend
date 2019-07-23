<template>
  <div class="main">
    <Row style="margin-top:20px;">
      <Col span="2" offset="5">
        <h1>任务列表</h1>
      </Col>
      <Col span="2" offset="18">
        <Button type="primary" shape="circle" icon="md-add" @click="newTaskModal">新建任务</Button>
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
        <Card v-for="(task, index) in taskList" :bordered="false" style="margin:5px;" v-on:click.native="getTask(index)">
          <Row>
            <Col span="4">{{ task.id }}</Col>
            <Col span="10">{{ task.instance }}</Col>
            <Col span="5">{{ task.state }}</Col>
            <Col span="5">{{ task.create_time }}</Col>
          </Row>
        </Card>
      </Col>
    </Row>
    <Modal v-model="getTaskModal" title="任务详情">
      <p>任务id：{{ taskInfo.id }}</p>
      <p>任务实例id：{{ taskInfo.instance }}</p>
      <p>地名：{{ taskInfo.place }}</p>
      <p>任务创建时间：{{ taskInfo.create_time }}</p>
      <p>任务状态：{{ taskInfo.state }}</p>
      <p v-if="taskInfo.ready==true">任务结果：{{ taskInfo.result }}</p>
    </Modal>
    <Modal v-model="postTaskModal" title="创建任务">
    </Modal>
  </div>
</template>

<script>
export default {
  name: 'Main',
  data () {
    return {
      taskList: [],
      getTaskModal: false,
      taskInfo: {},
      postTaskModal: false
    }
  },
  mounted () {
    this.getTaskList()
  },
  methods: {
    getTaskList() {
      this.$http.get("/api/task").then(res => {
        for (var i = 0; i < res.data.data.length; i++) {
          this.taskList.push(res.data.data[i])
        }
      }).catch(err => {
        console.log(err)
      })
    },
    newTaskModal () {
      this.postTaskModal = true
    },
    newTask () {
      console.log("new task")
      /*this.$http.post("/api/task").then(res => {
        //
      }).catch(err => {
        console.log(err)
      })*/
    },
    getTask (index) {
      console.log("get task")
      this.$http.get("/api/task/"+this.taskList[index].instance).then(res => {
        this.getTaskModal = true
        this.taskInfo.ready = res.data.ready
        this.taskInfo.state = res.data.state
        this.taskInfo.id = res.data.data.id
        this.taskInfo.instance = res.data.data.instance
        this.taskInfo.place = res.data.data.place
        this.taskInfo.create_time = res.data.data.create_time
        if (res.data.ready == true) this.taskInfo.result = res.data.result
      }).catch(err => {
        console.log(err)
      })
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
