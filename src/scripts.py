import sys
import os

base_path = sys.argv[1]
operation = sys.argv[2][0]
folder = sys.argv[2][-1]
name = sys.argv[3]
class_name = name.capitalize()

def main():
    try:
        if operation == 'g':
            print("Start generating...")
            index()
            styled()
            store()
            print(class_name, "is generated successfully.")
            stores = getAllStores()
            updateStore(stores)
            print("Store is updated successfully.")
        elif operation == 'r':
            print("Start removing...")
            # command = "cd src/components"
            # os.system(command)
        
    except Exception as e:
        print("operation fails:", e)

def get_src_folder_path():
    return os.path.join(base_path, "src")

def get_store_folder_path():
    return os.path.join(get_src_folder_path(), "store")

def get_folder_path():
    if folder == 'c':
        folder_name = "src/components/" + class_name
    elif folder == 'p':
        folder_name = "src/pages/" + class_name
    return os.path.join(base_path, folder_name)

def index():
    folder_path = get_folder_path()
    os.makedirs(folder_path)

    file_path = os.path.join(folder_path, "index.js")
    template = """import React, {{ Component }} from "react";
import {{ connect }}from "react-redux";
import {{}} from "./style";

class {class_name} extends Component {{
  render() {{
    return <div>{class_name}</div>;
  }}
}}

const mapStateToProps = state => {{
  return {{}};
}};

const mapDispatchToProps = dispatch => {{
  return {{}};
}};
export default connect(
  mapStateToProps,
  mapDispatchToProps
)({class_name});

"""

    context = {
        "class_name": class_name
    }
    with open(file_path, "w") as file:
        file.write(template.format(**context))
    print(file_path, "is successful.")

def styled():
    folder_path = get_folder_path()
    file_path = os.path.join(folder_path, "style.js")
    content = 'import styled from "styled-components";\n'
    with open(file_path, "w") as file:
        file.write(content)
    print(file_path, "is successful.")

def store():
    folder_path = get_folder_path()
    store_folder = os.path.join(folder_path, "store")
    os.makedirs(store_folder)

    flush_index(store_folder)
    flush_reducer(store_folder)
    flush_saga(store_folder)
    flush_creator(store_folder)
    flush_type(store_folder)
    print(store_folder, "is successful.")

def flush_index(folder_path):
    file_path = os.path.join(folder_path, "index.js")

    template = """import reducer from "./reducer";
import saga from "./saga";
import * as actionCreators from "./actionCreator";
import * as actionTypes from "./actionType";

export { reducer, saga, actionCreators, actionTypes };

"""
    with open(file_path, "w") as file:
        file.write(template)

def flush_reducer(folder_path):
    file_path = os.path.join(folder_path, "reducer.js")

    template = """import * as actionTypes from "./actionType";

const defaultState = {};

const reducer_handlers = {
  // [actionTypes.FOO]: (state, action) => {
  //   console.log("reducer:", action.type);
  //   return state;
  // }
};

export default (state = defaultState, action) => {
  if (reducer_handlers.hasOwnProperty(action.type)) {
    console.log("action type: ", action.type);
    return reducer_handlers[action.type](state, action);
  }
  return state;
};

"""
    with open(file_path, "w") as file:
        file.write(template)

def flush_saga(folder_path):
    file_path = os.path.join(folder_path, "saga.js")

    template = """import { put, takeEvery, all, call } from "redux-saga/effects";
import * as actionTypes from "./actionType";

const saga_handlers = {
  // [actionTypes.FOO]: function*(action) {
  //   try {
  //     console.log("saga:", action);
  //     yield put({});
  //   } catch (e) {
  //     console.log(e);
  //   }
  // }
};

function* saga() {
  yield all([
    takeEvery(
      action => {
        return saga_handlers.hasOwnProperty(action.type) ? action.type : "";
      },
      action => {
        return saga_handlers[action.type](action);
      }
    )
  ]);
}

export default saga;

"""
    with open(file_path, "w") as file:
        file.write(template)

def flush_creator(folder_path):
    file_path = os.path.join(folder_path, "actionCreator.js")

    template = """import * as actionTypes from './actionType';

// export const foo = () => ({
//     type: actionTypes.FOO
// }); 

"""
    with open(file_path, "w") as file:
        file.write(template)

def flush_type(folder_path):
    file_path = os.path.join(folder_path, "actionType.js")

    template = """// export const FOO = "{name}_foo";
"""
    context = {
        "name": name
    }
    with open(file_path, "w") as file:
        file.write(template.format(**context))

def getAllStores():
    # for root, dirs, files in os.walk("./src"):
    #     path = root.split(os.sep)
    #     print((len(path) - 1) * '---', os.path.basename(root))
    stores = {}
    for component in os.listdir("./src/components"): 
        stores[component] = 'components'
    for page in os.listdir("./src/pages"): 
        stores[page] = 'pages'
    return stores

def updateStore(stores):
    folder_path = get_store_folder_path()

    reducer_file = os.path.join(folder_path, "reducer.js")
    with open(reducer_file, "w") as file:
        file.write('import { combineReducers } from "redux";\n')
        for key, val in stores.items():
            line = 'import {{ reducer as {}Reducer }} from "../{}/{}/store"\n'.format(key, val, key)
            # print(line)
            file.write(line)
        file.write('\n')
        file.write('export default combineReducers({\n')
        for key, val in stores.items():
            line = '  {}: {}Reducer,\n'.format(key, key)
            file.write(line)
        file.write("});\n")

    saga_file = os.path.join(folder_path, "saga.js")
    with open(saga_file, "w") as file:
        file.write('import { fork, all } from "redux-saga/effects";\n')
        for key, val in stores.items():
            line = 'import {{ saga as {}Saga }} from "../{}/{}/store"\n'.format(key, val, key)
            file.write(line)
        file.write('\n')
        file.write('function* rootSaga(config) {\n')
        file.write('  yield all([\n')
        
        for key, val in stores.items():
            line = '    fork({}Saga),\n'.format(key)
            file.write(line)
        file.write("  ]);\n")
        file.write("}\n\n")
        file.write("export default rootSaga;\n")

main()