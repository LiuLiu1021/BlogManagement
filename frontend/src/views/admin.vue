<template>
  <div class="app-container">
    <!-- 查询和其他操作 -->
    <div class="filter-container" style="margin: 65px 0 10px 0;">
      <el-button class="filter-item" type="primary" icon="el-icon-edit" @click="changeReportState">举报信息管理</el-button>
      <el-button class="filter-item" type="warning" icon="el-icon-star-on" @click="changeActivityState">活动信息管理
      </el-button>
      <el-button v-if="add_visible" class="filter-item" type="primary" icon="el-icon-edit" @click="handleAdd">添加活动
      </el-button>
    </div>
    <el-table v-if="report_visible" :data="tableData" style="width: 100%" @selection-change="handleSelectionChange">
      <el-table-column type="selection"/>
      <el-table-column label="序号" width="60" align="center">
        <template slot-scope="scope">
          <span>{{ scope.$index + 1 }}</span>
        </template>
      </el-table-column>

      <el-table-column label="举报用户用户名" width="180" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.uid }}</span>
        </template>
      </el-table-column>

      <el-table-column label="被举报博客名称" width="180" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.title }}</span>
        </template>
      </el-table-column>

      <el-table-column label="举报理由" width="150" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.reason }}</span>
        </template>
      </el-table-column>

      <el-table-column label="举报时间" width="150" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.time }}</span>
        </template>
      </el-table-column>

      <el-table-column label="举报状态" width="150" align="center">
        <template slot-scope="scope">
          <template v-if="scope.row.status == 0">
            <span>未审核</span>
          </template>
          <template v-if="scope.row.status == 1">
            <span>举报成功</span>
          </template>
          <template v-if="scope.row.status == 2">
            <span>举报失败</span>
          </template>
        </template>
      </el-table-column>

      <el-table-column label="操作" fixed="right" min-width="230">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="handlePass(scope.row)">审核成功
          </el-button>
          <el-button type="error" size="small" @click="handleFail(scope.row)">审核失败
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-table v-if="activity_visible" :data="tableData" style="width: 100%" @selection-change="handleSelectionChange">
      <el-table-column type="selection"/>
      <el-table-column label="序号" width="60" align="center">
        <template slot-scope="scope">
          <span>{{ scope.$index + 1 }}</span>
        </template>
      </el-table-column>

      <el-table-column label="管理员用户名" width="100" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.uid }}</span>
        </template>
      </el-table-column>

      <el-table-column label="活动名称" width="150" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.sortName }}</span>
        </template>
      </el-table-column>

      <el-table-column label="起始时间" width="150" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.startTime }}</span>
        </template>
      </el-table-column>

      <el-table-column label="终止时间" width="150" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.endTime }}</span>
        </template>
      </el-table-column>

      <el-table-column label="奖励个人积分" width="200" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.credit }}</span>
        </template>
      </el-table-column>

      <!--      <el-table-column label="操作" fixed="right" min-width="230">-->
      <!--        <template slot-scope="scope">-->
      <!--          <el-button v-permission="'/blogSort/stick'" type="warning" size="small" @click="handleStick(scope.row)">审核成功</el-button>-->
      <!--          <el-button v-permission="'/blogSort/edit'" type="primary" size="small" @click="handleEdit(scope.row)">审核失败</el-button>-->
      <!--        </template>-->
      <!--      </el-table-column>-->
    </el-table>

    <!--分页-->
    <div class="block">
      <el-pagination
        :current-page.sync="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next, jumper"
        @current-change="handleCurrentChange"
      />
    </div>
    <el-dialog :title="title" :visible.sync="dialogFormVisible">
      <el-form ref="form" :model="form" :rules="rules">
        <el-form-item :label-width="formLabelWidth" label="活动名" prop="sortName">
          <el-input v-model="form.sortName" auto-complete="off"/>
        </el-form-item>

        <el-form-item :label-width="formLabelWidth" label="活动介绍" prop="content">
          <el-input v-model="form.description" auto-complete="off"/>
        </el-form-item>

        <el-form-item :label-width="formLabelWidth" label="起始时间" prop="sort">
          <!--          <el-input v-model="form.startTime" auto-complete="off"/>-->
          <el-date-picker
            v-model="form.startTime"
            type="date"
            value-format="yyyy-MM-dd"
            :picker-options="expireTime"
            placeholder="选择日期">
          </el-date-picker>
        </el-form-item>

        <el-form-item :label-width="formLabelWidth" label="终止时间" prop="sort">
          <!--          <el-input v-model="form.endTime" auto-complete="off"/>-->
          <el-date-picker
            v-model="form.endTime"
            type="date"
            value-format="yyyy-MM-dd"
            :picker-options="expireEndTime"
            placeholder="选择日期">
          </el-date-picker>
        </el-form-item>

        <el-form-item :label-width="formLabelWidth" label="奖励个人积分" prop="sort">
          <el-input v-model="form.credit" auto-complete="off"/>
        </el-form-item>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitForm">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {deleteBatchBlogSort} from '@/api/blogSort'

import {getReportList, getSortList, workReport} from '../api/report'
import {addBlogSort} from '../api/blogSort'

export default {
  data () {
    return {
      expireTime: {
        disabledDate (date) {
          return date.getTime() <= Date.now()
        }
      },
      expireEndTime: {
        disabledDate (date) {
          return date.getTime() <= Date.now()
        }
      },
      add_visible: false,
      activity_visible: false,
      report_visible: true,
      multipleSelection: [], // 多选，用于批量删除
      tableData: [],
      keyword: '',
      currentPage: 1,
      pageSize: 10,
      total: 0, // 总数量
      title: '增加分类',
      dialogFormVisible: false, // 控制弹出框
      formLabelWidth: '120px',
      isEditForm: false,
      form: {
        sortName: '',
        description: '',
        startTime: '',
        endTime: '',
        credit: 0
      },
      rules: {
        sortName: [
          {required: true, message: '活动名称不能为空', trigger: 'blur'},
          {min: 1, max: 10, message: '长度在1到10个字符'}
        ]
        // startTime: [
        //   { required: true, message: '起始时间不能为空', trigger: 'blur' },
        //   { pattern: /^[0-9]\d*$/, message: '排序字段只能为自然数' }
        // ],
        // endTime: [
        //   { required: true, message: '结束时间不能为空', trigger: 'blur' },
        //   { pattern: /^[0-9]\d*$/, message: '排序字段只能为自然数' }
        // ]
      }
    }
  },
  created () {
    this.reportList()
  },
  methods: {
    reportList: function () {
      getReportList().then(response => {
        this.tableData = response.data.records
      }).catch(error => {
        console.log(error)
        this.tableData = [{
          uid: '1',
          blog_id: '1',
          title: 'test',
          reason: 'ghs',
          time: '2020-12-7',
          status: '0'
        }, {
          uid: '1',
          blog_id: '1',
          title: 'test',
          reason: 'ghs',
          time: '2020-12-7',
          status: '0'
        }]
      })
    },
    sortList: function () {
      getSortList().then(response => {
        this.tableData = response.data.records
      }).catch(error => {
        console.log(error)
        this.tableData = [{
          uid: '1',
          sortName: 'test',
          startTime: '2020-12-7',
          endTime: '2020-12-7',
          credit: 10
        }, { uid: '1',
          sortName: 'test',
          startTime: '2020-12-7',
          endTime: '2020-12-7',
          credit: 10}
        ]
      })
    },
    changeReportState: function () {
      this.report_visible = true
      this.activity_visible = false
      this.add_visible = false
      this.reportList()
    },
    changeActivityState: function () {
      this.report_visible = false
      this.activity_visible = true
      this.add_visible = true
      this.sortList()
    },
    handleAdd: function () {
      this.dialogFormVisible = true
      this.form = this.getFormObject()
    },
    handlePass: function (row) {
      row.status = 1
      let params = row
      workReport(params).then(response => {
        if (response.data.code == this.$ECode.SUCCESS) {
          this.$message({
            type: 'success',
            message: response.data.message
          })
          window.location.reload()
        }
      })
    },
    handleFail: function (row) {
      row.status = 2
      let params = row
      workReport(params).then(response => {
        if (response.data.code == this.$ECode.SUCCESS) {
          this.$message({
            type: 'success',
            message: response.data.message
          })
          window.location.reload()
        }
      })
    },
    handleDelete: function (row) {
      var that = this
      this.$confirm('此操作将把分类删除, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          var params = []
          params.push(row)
          deleteBatchBlogSort(params).then(response => {
            if (response.data.code == this.$ECode.SUCCESS) {
              this.$commonUtil.message.success(response.message)
            } else {
              this.$commonUtil.message.error(response.message)
            }
            that.blogSortList()
          })
        })
        .catch(() => {
          this.$commonUtil.message.info('已取消删除')
        })
    },
    getFormObject: function () {
      let formObject = {
        sortName: '',
        description: '',
        startTime: '',
        endTime: '',
        credit: 0
      }
      return formObject
    },
    handleDeleteBatch: function () {
      var that = this
      if (that.multipleSelection.length <= 0) {
        this.$commonUtil.message.error('请先选中需要删除的内容!')
        return
      }
      this.$confirm('此操作将把选中的分类删除, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          deleteBatchBlogSort(that.multipleSelection).then(response => {
            if (response.data.code == this.$ECode.SUCCESS) {
              this.$commonUtil.message.success(response.message)
            } else {
              this.$commonUtil.message.error(response.message)
            }
            that.blogSortList()
          })
        })
        .catch(() => {
          this.$commonUtil.message.info('已取消删除！')
        })
    },
    handleCurrentChange: function (val) {
      this.currentPage = val
      this.blogSortList()
    },
    submitForm: function () {
      this.$refs.form.validate((valid) => {
        if (!valid) {
          console.log('校验失败')
        } else {
          console.log(this.form)
          addBlogSort(this.form).then(response => {
            if (response.data.code == this.$ECode.SUCCESS) {
              this.$commonUtil.message.success(response.message)
              this.dialogFormVisible = false
              this.sortList()
            } else {
              this.$commonUtil.message.error(response.message)
            }
          })
        }
      })
    },
    // 改变多选
    handleSelectionChange (val) {
      this.multipleSelection = val
    }
  }
}
</script>
<style>

</style>
