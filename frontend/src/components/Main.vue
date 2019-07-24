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
    <Modal v-model="getTaskModal" fullscreen title="任务详情" @on-ok="ok">
      <p>任务id：{{ taskInfo.id }}</p>
      <p>任务实例id：{{ taskInfo.instance }}</p>
      <p>地名：{{ taskInfo.place }}</p>
      <p>任务创建时间：{{ taskInfo.create_time }}</p>
      <p>任务状态：{{ taskInfo.state }}</p>
      <div v-if="taskInfo.ready==true">
        <p>任务结果：</p>
        <div v-for="(image, index) in taskInfo.result">
          <img :src="image" />
        </diV>
      </div>
      <Button type="error" shape="circle" icon="ios-trash" @click="deleteTask()">删除任务</Button>
    </Modal>
    <Modal v-model="postTaskModal" title="创建任务" @on-ok="handleSubmit('formInLine')">
      <Form ref="formInLine" :model="formInLine" :rules="ruleInLine" inline>
        <FormItem prop="place">
          <Input type="text" v-model="formInLine.place" placeholder="地名">
            <Icon type="ios-planet" slot="prepend"></Icon>
          </Input>
        </FormItem>
      </Form>
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
      postTaskModal: false,
      formInLine: {
        place: '',
      },
      ruleInLine: {
        place: [
          { required: true, message: '请输入地名', trigger: 'blur' }
        ]
      }
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
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
          if (valid) {
              var data = {}
              data.place = this.formInLine.place
              this.$http.post("/api/task", data=data).then(res => {
                this.$Message.success("任务创建成功！")
                this.ok()
              }).catch(err => {
                console.log(err)
                this.$Message.error("任务创建失败！")
              })
          } else {
              this.$Message.error("请输入正确地名！");
          }
      })
    },
    getTask (index) {
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
    },
    deleteTask () {
      this.$http.delete("/api/task/"+this.taskInfo.instance).then(res => {
        this.$Message.success("任务删除成功！")
      }).catch(err => {
        console.log(err)
        this.$Message.error("任务删除失败！")
      })
    },
    ok () {
      this.taskList = []
      this.getTaskList()
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
