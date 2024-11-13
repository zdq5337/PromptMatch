import React, {useEffect, useState} from 'react';
import {Button, Card, Flex, Input, Layout, message, Select, Typography} from 'antd';
import styles from './model_prompt.module.less';
import {CaretRightOutlined, CommentOutlined, DeleteOutlined, PlusOutlined} from "@ant-design/icons";
import {getAllLargeModelBase} from "@/api/service/large-model.ts";
import {getAllKnowledgeBase} from "@/api/service/knowledge.ts";

const {Header, Footer, Sider, Content} = Layout;

const {Text, Link, Paragraph} = Typography;
const {TextArea} = Input;


interface PromptTemplate {
  id: number;
  promptValue?: string;
  modelName?: string;
  knowledgeId?: string;
  responses?: SceneResponse[];
}

interface SceneResponse {
  response: string;
}

interface Variable {
  id: number;
  name?: string;
  value?: string;
  // prompt?: Prompt[];
}

interface Scene {
  id: number;
  variables: Variable[];
}

interface DataStructure {
  scenes: Scene[];
}


const ModelPrompt: React.FC = () => {


  const [largeModelOptions, setLargeModelOptions] = useState<{ value: string, label: string }[]>([]);
  const [knowledgeOptions, setKnowledgeOptions] = useState<{ value: number, label: string }[]>([]);

  const [variableInputCount, setVariableInputCount] = useState(1);
  const [scenesCount, setScenesCount] = useState(1);
  const [variables, setVariables] = useState<Variable[]>([{id: 0, name: '', value: ''}]);
  const [scenes, setScenes] = useState([{id: 0, variables: variables}]);
  const [promptTemplates, setPromptTemplates] = useState<PromptTemplate[]>([
    {
      id: 0,
      promptValue: '',
      modelName: '',
      knowledgeId: '',
      responses: [{response: ''}]
    },
    {
      id: 1,
      promptValue: '',
      modelName: '',
      knowledgeId: '',
      responses: [{response: ''}]
    }
  ]);

  let oldScenes = scenes.map(scene => ({...scene, variables: variables}));


  const handleAddPromptTemplate = () => {
    setPromptTemplates([
      ...promptTemplates,
      {
        id: promptTemplates.length,
        promptValue: '',
        modelName: '',
        knowledgeId: '',
        responses: new Array(scenesCount).fill({response: ''})
      }
    ]);
  };

  const handleAddScene = () => {
    setScenesCount(scenesCount + 1);
    setScenes([
      ...oldScenes,
      {id: scenesCount, variables: variables}
    ]);

    setPromptTemplates(promptTemplates.map(template => ({
      ...template,
      responses: template.responses ? [...template.responses, {response: ''}] : [{response: ''}]
    })));

    console.log('scenes', scenes);
  };

  const handleMinusScene = (sceneIndex: number) => {
    setScenesCount(scenesCount - 1);
    setScenes(scenes.filter((_, i) => i !== sceneIndex));

    setPromptTemplates(promptTemplates.map(template => ({
      ...template,
      responses: template.responses ? template.responses.filter((_, i) => i !== sceneIndex) : []
    })));
  };

  const handlePlusClick = () => {
    setVariableInputCount(variableInputCount + 1);
    setVariables([...variables, {id: variableInputCount, name: ''}]);
  };

  const handleMinusClick = () => {
    setVariableInputCount(variableInputCount - 1);
    setVariables(variables.slice(0, -1));
  };

  const handleInputChange = (id: number, newName: string) => {
    setVariables(variables.map(variable => variable.id === id ? {id, name: newName} : variable));
  };

  const handleInputVariableChange = (sceneId: number, variableId: number, newValue: string) => {
    setScenes(scenes.map(scene =>
      scene.id === sceneId
        ? {
          ...scene,
          variables: scene.variables.map(variable => variable.id === variableId ? {
            ...variable,
            value: newValue
          } : variable)
        }
        : scene
    ));
  };


  useEffect(() => {
    setScenes(scenes.map(scene => ({...scene, variables: variables})));
  }, [variables]); // 只有当variables发生变化时，才会触发这个effect

  const handleModelNameChange = (value: string, index: number) => {
    const newPromptTemplates = [...promptTemplates];
    newPromptTemplates[index].modelName = value;
    setPromptTemplates(newPromptTemplates);
  };

  const handleKnowledgeIdChange = (value: string, index: number) => {
    const newPromptTemplates = [...promptTemplates];
    newPromptTemplates[index].knowledgeId = value;
    setPromptTemplates(newPromptTemplates);
  };

  const onSearchByLargeModel = (value: string) => {
    console.log('search:', value);
  };


  // 提取获取大模型列表的函数
  const fetchAllLargeModelBaseList = () => {
    getAllLargeModelBase().then(({data}) => {
      const options = data.map(item => ({
        value: item.vendor_name,
        label: item.vendor_name,
      }));
      setLargeModelOptions(options);
    });
  };

  // 提取知识库列表的函数
  const fetchAllKnowledgeBaseList = () => {
    getAllKnowledgeBase().then(({data}) => {
      const options = data.map(item => ({
        value: item.id,
        label: item.name,
      }));
      setKnowledgeOptions(options);
    });
  };

  useEffect(() => {
    fetchAllLargeModelBaseList();
    fetchAllKnowledgeBaseList();
  }, []);

  const validatePromptTemplate = (template: PromptTemplate) => {
    // 检查 promptValue, modelName, knowledgeId 是否都有值
    if (!template.promptValue) {
      message.error('请填入prompt参数');
      return false;
    }

    if (!template.modelName) {
      message.error('请选择要使用的模型');
      return false;
    }


    // 检查 promptValue 是否满足条件
    const promptValueRegex = /^[a-zA-Z0-9_\u4e00-\u9fa5{} \p{P}]+$/u;
    if (!promptValueRegex.test(template.promptValue)) {
      message.error('promptValue 只能包含数字、字母、下划线、中文和 {}');
      return false;
    }

    // 检查 scenes 中的 variables 的所有 value 数据
    for (const scene of scenes) {
      for (const variable of scene.variables) {
        if (!variable.value) {
          message.error('请确保所有的变量都有值');
          return false;
        }
      }
    }

    // 所有检查都通过
    return true;
  };

  const handleRunPromptTemplates = async (promptTemplate: PromptTemplate, scenes: Scene[]): Promise<PromptTemplate> => {
    const newPromptTemplate = {...promptTemplate};

    if (validatePromptTemplate(newPromptTemplate)) {
      await Promise.all(scenes.map(async (scene, i) => {
        const messageObj = {
          prompt_template: newPromptTemplate.promptValue,
          prompt_params: scene.variables.reduce((obj: { [key: string]: any }, variable) => {
            if (variable.name) {
              obj[variable.name] = variable.value;
            }
            return obj;
          }, {})
        };

        const message = JSON.stringify(messageObj);
        console.log('message', message);

        // TODO 后续写在配置文件中，进行区分
        // 查看是否有  newPromptTemplate.knowledgeId  没有的话置为0
        if (!newPromptTemplate.knowledgeId) {
          newPromptTemplate.knowledgeId = '0';
        }
        const websocket = new WebSocket('ws://127.0.0.1:7000/api/model-match/v1/prompt_chat?model_name=' + newPromptTemplate.modelName + '&knowledge_id=' + newPromptTemplate.knowledgeId);

        websocket.onopen = async () => {
          websocket.send(message);
        };

        let response = '';

        websocket.onmessage = (event) => {
          console.log('event', event);
          response += event.data;
          if (newPromptTemplate.responses) {
            newPromptTemplate.responses[i] = {response: response}; // 更新对应场景的response
          }

          console.log('newPromptTemplate.responses', newPromptTemplate.responses);

          // 更新 promptTemplates 数组
          const newPromptTemplates = promptTemplates.map(template =>
            template.id === newPromptTemplate.id ? newPromptTemplate : template
          );
          setPromptTemplates(newPromptTemplates);

          // 收到消息后关闭连接
          // websocket.close();
        };

        // websocket.onmessage = (event) => {
        //   console.log('event', event);
        //   response += event.data;
        //
        //   setPromptTemplates(prevTemplates => {
        //     return prevTemplates.map(template => {
        //       if (template.id === newPromptTemplate.id) {
        //         // 如果是当前的模板，我们创建一个新的模板对象，更新其 responses
        //         const newTemplate = {...template};
        //         if (newTemplate.responses) {
        //           newTemplate.responses[i] = {response: response};
        //         }
        //         return newTemplate;
        //       } else {
        //         // 如果不是���前的模板，我们直接返回原模板对象
        //         return template;
        //       }
        //     });
        //   });
        // };

        websocket.onclose = () => {
          console.log('WebSocket connection closed');
        };

        websocket.onerror = (error) => {
          console.error('WebSocket error: ', error);
        };
      }));
    }

    return newPromptTemplate;
  };

  return (
    <Flex align="start" gap="middle">
      <Layout className={styles.layoutStyle}>
        <Header className={styles.headerStyle}>
          <Button type="primary" icon={<CaretRightOutlined/>} className={styles.headerAllRunButton}
                  onClick={async () => {  // 添加 async 关键字
                    const allValid = promptTemplates.every(validatePromptTemplate);
                    if (allValid) {
                      const newPromptTemplates = await Promise.all(promptTemplates.map(async (template, index) => {
                        return await handleRunPromptTemplates(template, scenes);
                      }));
                      setPromptTemplates(newPromptTemplates);
                    }
                  }}

          >
            全部运行
          </Button>
          <Button type="primary" icon={<PlusOutlined/>} className={styles.headerAllRunButton}
                  onClick={handleAddPromptTemplate}>
            添加prompt
          </Button>
          <Button type="primary" icon={<PlusOutlined/>} className={styles.headerAllRunButton} onClick={handleAddScene}>
            添加场景
          </Button>
        </Header>
        <Layout>
          <Sider width="25%" className={styles.siderStyle}
                 style={{backgroundColor: "#f3f9fd", position: "sticky", left: "0"}}
          >
            <div className={styles.siderItem}>
              <div className={styles.promptItemTitle}>
                <div className={styles.promptTitle}>
                  <CommentOutlined className={styles.commentIcon}/>
                  <Text>提示变量</Text>
                </div>
              </div>

              {variables.map(({id, name}) => (
                <div key={id} className={styles.promptVariablesItem}>
                  <Input className={styles.promptVariablesInput} placeholder="请输入您要定义的变量" value={name}
                         onChange={e => handleInputChange(id, e.target.value)}
                  />

                  <Button type="primary" icon={<DeleteOutlined/>} className={styles.promptVariableDelete} onClick={handleMinusClick}>
                    删除
                  </Button>
                </div>
              ))}

              <div className={styles.addVariableDiv} onClick={handlePlusClick}>
                {/*<PlusOutlined className={styles.plusIcon}/>*/}
                {/*<Text className={styles.addVariableFont}>添加变量</Text>*/}
                <Button type="primary" icon={<PlusOutlined/>} className={styles.addVariable} onClick={handleMinusClick}>
                  添加变量
                </Button>
              </div>
            </div>


            {scenes.map(({id: sceneId, variables}, index) => (
              console.log('scenes', scenes, 'promptTemplates', promptTemplates),
                <div key={sceneId} className={styles.siderItem}>
                  <div className={styles.promptSceneDivTop}>
                    <Input defaultValue={`场景${sceneId + 1}`} className={styles.promptSceneInputTop}
                           variant="borderless"/>
                    <Button type="primary" icon={<DeleteOutlined/>} className={styles.contentPromptBottomButton}
                            onClick={() => handleMinusScene(index)}
                    >
                      删除
                    </Button>
                  </div>

                  {variables.map(({id: variableId, name, value}) => (
                    <div key={variableId} className={styles.promptVariableValue}>
                      <Text className={styles.promptVariableValueText}>
                        {name || '提示变量'}
                      </Text>
                      <Input className={styles.promptVariablesInput} placeholder="请输入当前变量的值"
                             value={value}
                             onChange={e => handleInputVariableChange(sceneId, variableId, e.target.value)}
                      />
                    </div>
                  ))}
                </div>
            ))}
          </Sider>


          <Content className={styles.contentStyle}>
            <div className={styles.contentDivFather}>
              {promptTemplates.map((template, index) => (
                console.log('promptTemplates11111111111111', promptTemplates),
                  <div key={index} className={styles.contentDiv}>
                    <div className={styles.contentSubElementDiv}>
                      <div className={styles.contentPromptTop}>
                        <Input value={`Prompt${template.id + 1}`} className={styles.contentPromptTopDiv}
                               variant="borderless"/>
                        <Select
                          showSearch
                          variant="filled"
                          placeholder="选择您要使用的模型"
                          optionFilterProp="label"
                          onChange={(value) => handleModelNameChange(value, index)}
                          // onSearch={onSearchByLargeModel}
                          options={largeModelOptions}
                          value={template.modelName || template.modelName === '' ? undefined : template.modelName}
                        />
                        <Select
                          showSearch
                          variant="borderless"
                          placeholder="选择您的知识库"
                          optionFilterProp="label"
                          onChange={(value) => handleKnowledgeIdChange(value, index)}
                          // onSearch={onSearchByLargeModel}
                          options={knowledgeOptions}
                          value={template.knowledgeId || template.knowledgeId === '' ? undefined : template.knowledgeId}
                        />
                      </div>
                      <TextArea
                        // autoSize
                        size={"middle"}
                        placeholder={"//请填写您的prompt内容, 添加prompt模板"}
                        showCount={true}
                        maxLength={1000}
                        variant="filled"
                        className={styles.contentInputTextArea}
                        value={template.promptValue}
                        onChange={e => {
                          const newPromptTemplates = [...promptTemplates];
                          newPromptTemplates[index].promptValue = e.target.value;
                          setPromptTemplates(newPromptTemplates);
                        }}
                      />
                      <div className={styles.contentPromptBottom}>

                        <div>
                          <Button type="primary" icon={<CaretRightOutlined/>}
                                  className={styles.contentPromptBottomRunButton}
                                  onClick={async () => {  // 添加 async 关键字
                                    if (validatePromptTemplate(promptTemplates[index])) {
                                      const newPromptTemplate = await handleRunPromptTemplates(promptTemplates[index], scenes);
                                      const newPromptTemplates = [...promptTemplates];
                                      newPromptTemplates[index] = newPromptTemplate;
                                      setPromptTemplates(newPromptTemplates);
                                      console.log('promptTemplates2222222', promptTemplates);
                                    }

                                  }}
                          >
                            单独运行
                          </Button>
                        </div>
                        <div>
                          <Button type="primary" icon={<DeleteOutlined/>} className={styles.contentPromptBottomDeleteButton}
                                  onClick={() => {
                                    console.log('delete', index);
                                    setPromptTemplates(promptTemplates.filter((_, i) => i !== index));
                                  }}>
                            删除
                          </Button>
                        </div>

                      </div>
                    </div>

                    {template.responses && template.responses.map((res, resIndex) => (
                      <div className={styles.contentSubElementResponseDiv}>
                        <Card key={resIndex} title={"Response"} className={styles.contentSubElementCard}
                              bordered={false}>
                          <div className={styles.responseCardDiv}>
                            <Paragraph className={styles.responseParagraph}>
                              {res.response || "这里来放置响应的数据"}
                            </Paragraph>
                          </div>

                        </Card>
                      </div>
                    ))}

                  </div>
              ))}

            </div>
          </Content>
        </Layout>

      </Layout>
    </Flex>
  )
};

export default ModelPrompt;
