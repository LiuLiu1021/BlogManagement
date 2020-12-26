<template>
  <div class="app-container">
    <!-- 添加或修改对话框 -->
    <el-dialog
      :title="title"
      :visible.sync="dialogFormVisible"
      :before-close="closeDialog"
      fullscreen
    >
      <el-form ref="form" :model="form" :rules="rules">
        <el-row>
          <el-col >
            <el-form-item :label-width="formLabelWidth" label="标题" prop="title">
              <el-input v-model="form.title" auto-complete="off" @input="contentChange"/>
            </el-form-item>
            <el-form-item :label-width="formLabelWidth" label="简介">
              <el-input v-model="form.summary" auto-complete="off" />
            </el-form-item>
          </el-col>

<!--          <el-col :span="8">-->
<!--            <el-form-item :label-width="formLabelWidth" label="标题图">-->
<!--              <div v-if="form.photoList" class="imgBody">-->
<!--                <i-->
<!--                  v-show="icon"-->
<!--                  class="el-icon-error inputClass"-->
<!--                  @click="deletePhoto()"-->
<!--                  @mouseover="icon = true"-->
<!--                />-->
<!--                <img-->
<!--                  :src="form.photoList[0]"-->
<!--                  style="display:inline; width: 195px;height: 105px;"-->
<!--                  @mouseover="icon = true"-->
<!--                  @mouseout="icon = false"-->
<!--                >-->
<!--              </div>-->
<!--              <div v-else class="uploadImgBody" @click="checkPhoto">-->
<!--                <i class="el-icon-plus avatar-uploader-icon"/>-->
<!--              </div>-->
<!--            </el-form-item>-->
<!--          </el-col>-->
        </el-row>

        <el-row>
          <el-col :span="6.5">
            <el-form-item :label-width="formLabelWidth" label="活动" prop="blogSortUid">
              <el-select
                v-model="form.blogSortUid"
                size="small"
                placeholder="请选择"
                style="width:150px"
              >
                <el-option
                  v-for="item in blogSortData"
                  :key="item.uid"
                  :label="item.name"
                  :value="item.uid"
                />
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="6.5">
            <el-form-item label="标签" label-width="80px">
              <el-select
                v-model="tagValue"
                multiple
                size="small"
                placeholder="请选择"
                style="width:210px"
                filterable
              >
                <el-option
                  v-for="item in tagData"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6.5">
            <el-form-item label="所需积分" label-width="80px">
              <el-input v-model="form.need_credit" auto-complete="off" @input="contentChange"/>
            </el-form-item>
          </el-col>
<!--          <el-col :span="6.5">-->
<!--            <el-form-item :label-width="maxLineLabelWidth" label="推荐等级" prop="level">-->
<!--              <el-select v-model="form.level" size="small" placeholder="请选择" style="width:210px">-->
<!--                <el-option-->
<!--                  v-for="item in blogLevelDictList"-->
<!--                  :key="item.uid"-->
<!--                  :label="item.dictLabel"-->
<!--                  :value="parseInt(item.dictValue)"-->
<!--                />-->
<!--              </el-select>-->
<!--            </el-form-item>-->
<!--          </el-col>-->
        </el-row>

<!--        <el-row>-->
<!--          <el-col :span="6.5">-->
<!--            <el-form-item :label-width="formLabelWidth" label="是否原创" prop="isOriginal">-->
<!--              <el-radio-group v-model="form.isOriginal" size="small">-->
<!--                <el-radio v-for="item in blogOriginalDictList" :key="item.uid" :label="item.dictValue" border>{{ item.dictLabel }}</el-radio>-->
<!--              </el-radio-group>-->
<!--            </el-form-item>-->
<!--          </el-col>-->

<!--          <el-col :span="6.5">-->
<!--            <el-form-item :label-width="formLabelWidth" label="文章类型" prop="openComment">-->
<!--              <el-radio v-for="item in blogTypeDictList" :key="item.uid" v-model="form.type" :label="item.dictValue" border size="small">{{ item.dictLabel }}</el-radio>-->
<!--            </el-form-item>-->
<!--          </el-col>-->

<!--          <el-col :span="6.5">-->
<!--            <el-form-item :label-width="formLabelWidth" label="文章评论" prop="openComment">-->
<!--              <el-radio v-for="item in openDictList" :key="item.uid" v-model="form.openComment" :label="item.dictValue" border size="small">{{ item.dictLabel }}</el-radio>-->
<!--            </el-form-item>-->
<!--          </el-col>-->

<!--          <el-col :span="4.5">-->
<!--            <el-form-item :label-width="lineLabelWidth" label="是否发布" prop="isPublish">-->
<!--              <el-radio-group v-model="form.isPublish" size="small">-->
<!--                <el-radio v-for="item in blogPublishDictList" :key="item.uid" :label="item.dictValue" border>{{ item.dictLabel }}</el-radio>-->
<!--              </el-radio-group>-->
<!--            </el-form-item>-->
<!--          </el-col>-->
<!--        </el-row>-->

        <el-form-item :label-width="formLabelWidth" label="内容" prop="content">
          <ckeditor v-if="systemConfig.editorModel == '0'" ref="editor" v-model="form.content" :height="360"/>
          <MarkdownEditor v-if="systemConfig.editorModel == '1'" ref="editor" :content="form.content" :height="465"/>
        </el-form-item>

        <el-form-item style="float: right; margin-right: 20px;">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitForm">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { addBlog, editBlog } from '@/api/blog'
// import { getSystemConfig } from '@/api/systemConfig'
import { getTagList } from '@/api/tag'
import { getBlogSortList } from '@/api/blogSort'
// import { formatData } from '@/utils/webUtils'
// import { getToken } from '@/utils/auth'
// import { getToken } from '@/utils/auth'
// import { setCookie, getCookie, delCookie } from '@/utils/cookieUtils'
// import { getListByDictTypeList } from '@/api/sysDictData'
// import { addSubjectItemList } from '@/api/subjectItem'

// import CheckPhoto from '../../components/CheckPhoto'
// import CKEditor from '../components/CKEditor'
import MarkdownEditor from '../components/MarkdownEditor'
// import SubjectSelect from '../../components/SubjectSelect'
// var querystring = require('querystring')
import { mapGetters } from 'vuex'
import { Loading } from 'element-ui'
export default {
  computed: {
    ...mapGetters(['name', 'roles'])
  },
  components: {
    MarkdownEditor
  },
  data () {
    return {
      uploadLoading: null, // 文件上传loading
      CKEditorData: null,
      tableData: [], // 博客数据
      tagData: [], // 标签数据
      tagValue: [], // 保存选中标签id(编辑时)
      blogSortData: [{uid: 1, name: '技术'}, {uid: 2, name: '大数据'}],
      title: '增加博客',
      dialogFormVisible: true, // 控制弹出框
      subjectVisible: false, // 是否显示专题
      isFirstSubjectVisible: true, // 专题选择器是否首次显示【用于懒加载】
      formLabelWidth: '120px',
      lineLabelWidth: '120px', // 一行的间隔数
      maxLineLabelWidth: '100px',
      isEditForm: false,
      photoVisible: false, // 控制图片选择器的显示
      isFirstPhotoVisible: true, // 图片选择器是否首次显示【用于懒加载】
      photoList: [],
      fileIds: '',
      icon: false, // 控制删除图标的显示
      interval: null, // 定义触发器
      isChange: false, // 表单内容是否改变
      changeCount: 0, // 改变计数器
      blogOriginalDictList: [], // 存储区域字典
      blogPublishDictList: [], // 是否字典
      blogLevelDictList: [], // 博客推荐等级字典
      openDictList: [], // 是否启动字典
      blogTypeDictList: [], // 文章类型字典
      blogOriginalDefault: null, // 博客原创默认值
      blogLevelDefault: null, // 博客等级默认值
      blogPublishDefault: null, // 博客发布默认值
      openDefault: null, // 是否开启评论默认值
      blogTypeDefault: null, // 文章类型默认值
      fileList: [],
      localUploadVisible: false,
      systemConfig: {editorModel: 0}, // 系统配置
      form: {
        title: '',
        summary: '',
        content: '',
        tagUid: '',
        blogSortUid: '',
        isOriginal: '', // 是否原创
        isPublish: '',
        author: '', // 作者
        clickCount: 0,
        articlesPart: '', // 文章出处
        need_credit:''
      },
      rules: {
        title: [
          { required: true, message: '标题不能为空', trigger: 'blur' }
        ],
        blogSortUid: [
          { required: true, message: '分类不能为空', trigger: 'blur' }
        ],
        level: [
          { required: true, message: '推荐等级不能为空', trigger: 'blur' },
          { pattern: /^[0-9]\d*$/, message: '推荐等级只能为自然数' }
        ],
        isPublish: [
          { required: true, message: '发布字段不能为空', trigger: 'blur' },
          { pattern: /^[0-9]\d*$/, message: '发布字段只能为自然数' }
        ],
        isOriginal: [
          { required: true, message: '原创字段不能为空', trigger: 'blur' },
          { pattern: /^[0-9]\d*$/, message: '原创字段只能为自然数' }
        ],
        openComment: [
          { required: true, message: '网站评论不能为空', trigger: 'blur' },
          { pattern: /^[0-9]\d*$/, message: '网站评论只能为自然数' }
        ],
        content: [
          { required: true, message: '内容不能为空', trigger: 'blur' }
        ],
        outsideLink: [
          { required: true, message: '外链地址不能为空', trigger: 'blur' },
          { pattern: /^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+/, message: '请输入有效的URL' }
        ]
      }
    }
  },
  created () {
    console.log('-----------------------------------------')
    this.title = '增加博客'
    //  const that = this
    // // const tempForm = JSON.parse(getCookie('form'))
    //  const tempForm=null
    //  if (tempForm != null && tempForm.title != null && tempForm.title != '') {
    //    this.$confirm('还有上次未完成的博客编辑，是否继续编辑?', '提示', {
    //      confirmButtonText: '确定',
    //      cancelButtonText: '取消',
    //      type: 'warning'
    //    }).then(() => {
    //      that.dialogFormVisible = true
    //      that.tagValue = []
    //      that.form = JSON.parse(getCookie('form'))
    //      var tagValue = that.form.tagUid.split(',')
    //      for (var a = 0; a < tagValue.length; a++) {
    //        if (tagValue[a] != null && tagValue[a] != '') {
    //          that.tagValue.push(tagValue[a])
    //        }
    //      }
    //      if (that.form.uid) {
    //        that.title = '编辑博客'
    //        that.isEditForm = true
    //      } else {
    //        that.title = '新增博客'
    //        that.isEditForm = false
    //      }
    //    })
    //      .catch(() => {
    //        that.dialogFormVisible = true
    //        that.form = that.getFormObject()
    //        that.$nextTick(() => {
    //          // DOM现在更新了
    //          that.$refs.editor.setData(that.form.content) // 设置富文本内容
    //        })
    //        that.tagValue = []
    //        that.isEditForm = false
    //        that.title = '新增博客'
    //        delCookie('form')
    //      })
    //  } else {
    //    that.dialogFormVisible = true
    //    that.form = this.getFormObject()
    //
    //    that.$nextTick(() => {
    //      // 初始化内容
    //      that.$refs.editor.initData()
    //    })
    //
    //    that.tagValue = []
    //    that.isEditForm = false
    //    that.formBak()

    // 从dashboard传递过来的 tagUid 以及 blogSortUid
    // const tempTag = this.$route.query.tag
    // const tempBlogSort = this.$route.query.blogSort
    //
    // if (tempTag != undefined) {
    //   this.tagRemoteMethod(tempTag.name)
    //   this.queryParams.tagKeyword = tempTag.tagUid
    // }
    // if (tempBlogSort != undefined) {
    //   this.sortRemoteMethod(tempBlogSort.name)
    //   this.queryParams.sortKeyword = tempBlogSort.blogSortUid
    // }
    //
    // // 判断是否需要展开条件查询
    // this.getShowSearch()
    //
    // // 获取系统配置
    // this.getSystemConfigList()
    //
    // // 获取字典
    // this.getDictList()
    //
    // // 获取标签列表
    this.tagList()
    //
    // // 获取博客分类
    this.blogSortList()
    //
    // // 获取博客列表
    // this.blogList()
  },
  methods: {
    openLoading () {
      this.uploadLoading = Loading.service({
        lock: true,
        text: '正在努力上传中……'
      })
    },
    closeLoading () {
      this.uploadLoading.close()
    },
    tagList: function () {
      getTagList().then(response => {
        this.tagData = response.data.records
      }).catch(error => {
        console.log(error)
        this.tagData = [{uid: 1, content: '技术'}, {uid: 2, content: '大数据'}]
      })
    },
    blogSortList: function () {
      getBlogSortList().then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          this.blogSortData = response.data.records
        }
      }).catch(error => {
        console.log(error)
        this.blogSortData = [{uid: 1, name: '技术'}, {uid: 2, name: '大数据'}]
      })
    },
    // getFormObject: function () {
    //   var formObject = {
    //     uid: null,
    //     title: 'null',
    //     summary: null,
    //     content: null,
    //     tagUid: null,
    //     fileUid: null,
    //     isOriginal: this.blogOriginalDefault, // 是否原创
    //     isPublish: this.blogOriginalDefault, // 是否发布
    //     type: this.blogTypeDefault, // 文章类型
    //     author: null, // 作者
    //     level: parseInt(this.blogLevelDefault), // 推荐等级，默认是正常
    //     openComment: this.openDefault, // 是否启动
    //     articlesPart: null // 文章出处，默认蘑菇博客
    //   }
    //   return formObject
    // },
    // 获取系统配置
    // getSystemConfigList: function () {
    //   getSystemConfig().then(response => {
    //     if (response.code == this.$ECode.SUCCESS) {
    //       if (response.data) {
    //         this.systemConfig = response.data
    //       }
    //     }
    //   })
    // },
    // 关闭窗口
    closeDialog (done) {
      if (this.isChange) {
        this.$confirm('是否关闭博客编辑窗口', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            // 清空触发器
            clearInterval(this.interval)
            this.isChange = false
            this.changeCount = 0
            this.$router.go(-1)
            // done()
          })
          .catch(() => {
            this.$commonUtil.message.info('已取消')
          })
      } else {
        // 清空触发器
        clearInterval(this.interval)
        this.isChange = false
        this.changeCount = 0
        this.$router.go(-1)
        // done()
      }
    },

    // 内容改变，触发监听
    contentChange: function () {
      // console.log(this.form.content = this.$refs.editor.getData()) // 获取CKEditor中的内容
      // console.log("!!!!!!!!!!!!!!")
      // console.log(this.form.content)
      // this.$forceUpdate()
      // var that = this
      // if (this.changeCount > 0) {
      //   that.isChange = true
      //   // // 存放到cookie中，时间10天
      //   // that.form.content = that.$refs.editor.getData() // 获取CKEditor中的内容
      //   // that.form.tagUid = that.tagValue.join(',')
      //   // setCookie('form', JSON.stringify(that.form), 10)
      // }
      // this.changeCount = this.changeCount + 1
    },
    // // 备份form表单
    // formBak: function () {
    //   var that = this
    //   that.interval = setInterval(function () {
    //     if (that.form.title != null && that.form.title != '') {
    //       // 存放到cookie中，时间10天
    //       that.form.content = that.$refs.editor.getData() // 获取CKEditor中的内容
    //       that.form.tagUid = that.tagValue.join(',')
    //       setCookie('form', JSON.stringify(that.form), 10)
    //     }
    //   }, 10000)
    // },
    handleCurrentChange: function (val) {
      this.currentPage = val
      this.blogList()
    },
    submitForm: function () {
      if (this.tagValue.length <= 0) {
        this.$commonUtil.message.error('标签不能为空!')
        return
      }
      this.$refs.form.validate((valid) => {
        if (!valid) {
        } else {
          this.form.tagUid = this.tagValue.join(',')
          if (this.isEditForm) {
            editBlog(this.form).then(response => {
              if (response.data.code === this.$ECode.SUCCESS) {
                this.$commonUtil.message.success(response.message)
                // 清空cookie中的内容
                // delCookie('form')
                this.dialogFormVisible = false
                this.blogList()
              } else {
                this.$commonUtil.message.error(response.message)
              }
            })
          } else {
            addBlog(this.form).then(response => {
              if (response.data.code === this.$ECode.SUCCESS) {
                this.$commonUtil.message.success(response.message)
                // 清空cookie中的内容
                // delCookie('form')
                // 清空触发器
                clearInterval(this.interval)
                this.dialogFormVisible = false
                location.href=this.vueMoguWebUrl + '/#/'
              } else {
                this.$commonUtil.message.error(response.message)
              }
            })
          }
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
<style scoped>

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  margin: 0px 0px 0px 10px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width:  195px;
  height: 105px;
  line-height: 105px;
  text-align: center;
}
.imgBody {
  width:  195px;
  height: 105px;
  border: solid 2px #ffffff;
  float: left;
  position: relative;
}
.uploadImgBody {
  margin-left: 5px;
  width:  195px;
  height: 105px;
  border: dashed 1px #c0c0c0;
  float: left;
  position: relative;
}
.uploadImgBody :hover {
  border: dashed 1px #00ccff;
}
.inputClass {
  position: absolute;
}
.el-dialog__body {
  padding-top: 10px;
  padding-bottom: 0px;
}
.el-dialog {
  min-height: 400px;
}
.el-upload__tip {
  margin-top: 10px;
  margin-left: 10px;
  color: #3e999f;
}

.upload-demo {
  margin-top: 50px;
}
.tipBox {
  margin-bottom: 30px;
}
.tip {
  font-size: 14px;
  font-weight: bold;
  color: 	#808080;
}
.tipItem {
  line-height: 22px;
  color: 	#A9A9A9;
}
</style>
