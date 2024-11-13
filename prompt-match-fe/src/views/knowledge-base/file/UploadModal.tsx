import {forwardRef, useImperativeHandle, useState} from 'react'
import type {GetProp, UploadProps} from 'antd';
import {message, Modal, Upload} from 'antd'
import {InboxOutlined} from '@ant-design/icons';
import {UploadFile} from 'antd/lib/upload/interface';
import {useParams} from "react-router-dom";
import {createKnowledgeFile} from '@/api/service/knowledge.ts'
import {
  KnowledgeFileBaseListItemBase,
  KnowledgeFileBaseListItemType
} from "@/views/knowledge-base/list/knowledge-types";
import {ResponseData} from "@/types";

const {Dragger} = Upload;

export interface KnowledgeFileUploadModalHandle {
  open: () => void
  close: () => void
}

interface KnowledgeFileModalProps {
  fetchKnowledgeFileBase: () => void;
}


const KnowledgeFileUploadModal = forwardRef<KnowledgeFileUploadModalHandle, KnowledgeFileModalProps>((props, ref) => {

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<UploadFile[]>([]); // 用于保存上传成功的文件信息
  const [KnowledgeFiles, setKnowledgeFiles] = useState<KnowledgeFileBaseListItemType[]>([]); // 用于保存上传成功的文件信息
  // const [fileList, setFileList] = useState([]);

  type FileType = Parameters<GetProp<UploadProps, 'beforeUpload'>>[0];

  const showModal = () => {
    setIsModalOpen(true);
  };

  useImperativeHandle(ref, () => ({
    open: () => {
      setIsModalOpen(true);
    },
    close: () => {
      setIsModalOpen(false)
    }
  }))

  const handleOk = () => {
    // 这里要进行调用上传文件的接口
    createKnowledgeFile(KnowledgeFiles).then((responseData: ResponseData<any>) => {
      console.log(responseData); // 这里就是你的 ResponseData 数据
      if (responseData.code !== "000000") {
        message.error(responseData.message);
        return;
      }
      message.success('上传成功').then(r => console.log(r));
      props.fetchKnowledgeFileBase();

    })
    setIsModalOpen(false);
    setUploadedFiles([]); // 清除上传的文件记录
    setKnowledgeFiles([]); // 清除上传的文件记录
  };

  const handleCancel = () => {
    setUploadedFiles([]); // 清除上传的文件记录
    setKnowledgeFiles([]); // 清除上传的文件记录
    console.log("clink cancel")
    setIsModalOpen(false);

  };

  const {id: idString} = useParams();
  const id = Number(idString);

  const uploadProps: UploadProps = {
    name: 'file',
    multiple: true,
    // TODO 配置文件的方式
    action: 'http://127.0.0.1:7000/api/model-match/v1/file/upload?file_path=knowledge/rag',
    method: 'post',
    // accept: '.doc,.docx,.pdf,.xls,.xlsx,.ppt,.pptx,.txt,.zip,.rar,.7z,.jpg,.jpeg,.png,.gif,.bmp',
    accept: '.pdf,.PDF',
    maxCount: 1,
    // data: {"file_path": "knowledge/rag"},
    fileList: uploadedFiles,
    // fileList: fileList, // 添加fileList属性
    beforeUpload(file: FileType) {
      const isLt2M = file.size / 1024 / 1024 < 50;
      if (!isLt2M) {
        message.error('File must smaller than 50MB!');
      }
      return isLt2M;
    },
    onChange(info) {
      setUploadedFiles([info.file]); // 直接设置状态为最新上传成功的文件
      const {status} = info.file;
      if (status !== 'uploading') {
        console.log(info.file, info.fileList);
      }

      if (status === 'done') {
        console.log("file info", info.file);
        message.success(`${info.file.name} file uploaded successfully.`);
        // setUploadedFiles(prevFiles => [...prevFiles, info.file]); // 将上传成功的文件添加到状态中
        // 创建一个新的对象，包含文件的name和size属性
        const newFile: KnowledgeFileBaseListItemType = {
          name: info.file.name,
          oss_path: info.file.response.data.file_url,
          size: info.file.size !== undefined ? info.file.size : 0, // If info.file.size is undefined, assign 0
          knowledge_id: id,
          // 添加其他需要的属性...
        };
        setKnowledgeFiles(prevFiles => [...prevFiles, newFile]); // 将上传成功的文件添加到状态中
        console.log("newFile", newFile)
        console.log("id", id)
      } else if (status === 'error') {
        message.error(`${info.file.name} file upload failed.`);
      }
    },
    onDrop(e) {
      console.log('Dropped files', e.dataTransfer.files);
    },
  };


  return (
    <Modal title="上传文件"
           open={isModalOpen}
           onOk={handleOk}
           onCancel={handleCancel}
           okText='保存'
           cancelText='取消'>
      <Dragger {...uploadProps}>
        <p className="ant-upload-drag-icon">
          <InboxOutlined/>
        </p>
        <p className="ant-upload-text">单击或拖动文件到此区域进行上传</p>
        <p className="ant-upload-hint">
          支持单次或批量上传。严禁上传公司数据或其他被禁止的文件。（暂时只支持pdf文件上传）
        </p>
      </Dragger>
    </Modal>
  )
})

export default KnowledgeFileUploadModal
