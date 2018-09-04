import sys
import os
import shutil

base_path = sys.argv[1]
operation = sys.argv[2][0]
folder = sys.argv[2][-1]
name = sys.argv[3]
class_name = name.capitalize()
style_name = ''
tag_name = ''
if len(sys.argv) > 4:
    style_name = sys.argv[4]
    tag_name = sys.argv[5]


def main():
    try:
        if operation == 'g':
            print("Start generating...")
            index()
            styled()
            store()
            print(class_name, "is generated successfully.")
            stores = get_all_stores()
            updateStore(stores)
            print("Store is updated successfully.")
            import_all()
            print("import successfully.")
        elif operation == 'r':
            print("Start removing...")
            shutil.rmtree(get_folder_path())
            print(class_name, "is removed successfully.")
            stores = get_all_stores()
            updateStore(stores)
            print("Store is updated successfully.")
            import_all()
            print("import update successfully.")
        elif operation == 's':
            print("Start generating...")
            generate_style()
            print(style_name, "is generated successfully.")

    except Exception as e:
        print("operation fails:", e)


def generate_style():
    folder_path = get_folder_path()
    file_path = os.path.join(folder_path, "style.js")
    index = 0
    contents = []
    with open(file_path, "r") as file:
        contents = file.readlines()
    
    for idx, line in enumerate(contents):
        if line.strip().startswith("export"):
            index = idx
            break

    line = 'const {} = styled.{}`\n'.format(style_name, tag_name)
    contents.insert(index, line)
    line = '`;\n\n'
    contents.insert(index+1, line)
    line = '    {},\n'.format(style_name)
    contents.insert(-1, line)

    with open(file_path, "w") as file:
        file.writelines(contents)

def get_src_folder_path():
    return os.path.join(base_path, "src")


def get_store_folder_path():
    return os.path.join(get_src_folder_path(), "store")


def get_folder_path():
    if folder == 'c':
        folder_name = "src/components/" + class_name
    elif folder == 'p':
        folder_name = "src/pages/" + class_name
    elif folder == 's':
        stores = get_all_stores()
        folder_name = "src/" + stores[class_name] + "/" + class_name
    return os.path.join(base_path, folder_name)


def get_components_folder_path():
    return os.path.join(base_path, "src/components/")


def get_pages_folder_path():
    return os.path.join(base_path, "src/pages/")


def index():
    folder_path = get_folder_path()
    os.makedirs(folder_path)

    file_path = os.path.join(folder_path, "index.js")
    template = """import React, {{ PureComponent }} from "react";
import {{ connect }}from "react-redux";
import {{ actionCreators, selectors }} from "./store";
import {{ styles as s }} from "./style";

class {class_name} extends PureComponent {{
  render() {{
    return <div>{class_name}</div>;
  }}
}}

const mapStateToProps = state => {{
  return {{
      // foo: selectors.fooSelector(state)
  }};
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
    content = """import styled from "styled-components";\n
export const styles = { 
};
"""
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
    flush_selector(store_folder)
    print(store_folder, "is successful.")


def flush_index(folder_path):
    file_path = os.path.join(folder_path, "index.js")

    template = """import reducer from "./reducer";
import saga from "./saga";
import * as actionCreators from "./actionCreator";
import * as actionTypes from "./actionType";
import * as selectors from './selectors';

export { reducer, saga, actionCreators, actionTypes, selectors };

"""
    with open(file_path, "w") as file:
        file.write(template)


def flush_reducer(folder_path):
    file_path = os.path.join(folder_path, "reducer.js")

    template = """import * as actionTypes from "./actionType";
import { fromJS } from "immutable";

const defaultState = fromJS({});

const reducer_handlers = {
  // [actionTypes.FOO]: (state, action) => {
  //   console.log("reducer:", action.type);
  //   return state.set("key", val);
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


def flush_selector(folder_path):
    file_path = os.path.join(folder_path, "selectors.js")

    template = """import {{ createSelector }} from "reselect";

// const selectFoo = state => state.getIn(['{class_name}', 'foo']);
// export const fooSelector = createSelector(selectFoo, item => item);

"""
    context = {
        "class_name": class_name
    }
    with open(file_path, "w") as file:
        file.write(template.format(**context))


def get_all_components():
    components = []
    for component in os.listdir("./src/components"):
        if os.path.isdir(os.path.join('./src/components', component)):
            components.append(component)
    return components


def get_all_pages():
    pages = []
    for page in os.listdir("./src/pages"):
        if os.path.isdir(os.path.join('./src/pages', page)):
            pages.append(page)
    return pages


def get_all_stores():
    stores = {}
    components = get_all_components()
    pages = get_all_pages()
    for component in components:
        stores[component] = 'components'
    for page in pages:
        stores[page] = 'pages'
    return stores


def updateStore(stores):
    folder_path = get_store_folder_path()

    reducer_file = os.path.join(folder_path, "reducer.js")
    with open(reducer_file, "w") as file:
        file.write('import { combineReducers } from "redux-immutable";\n')
        for key, val in stores.items():
            line = 'import {{ reducer as {}Reducer }} from "../{}/{}/store"\n'.format(
                key, val, key)
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
            line = 'import {{ saga as {}Saga }} from "../{}/{}/store"\n'.format(
                key, val, key)
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


def import_all():
    if folder == 'c':
        component_index_file = os.path.join(
            get_components_folder_path(), "index.js")
        components = get_all_components()

        with open(component_index_file, "w") as file:
            for component in components:
                line = 'import {} from "./{}";\n'.format(component, component)
                file.write(line)
            file.write('\n')
            file.write('export {\n')
            for component in components:
                line = '    {},\n'.format(component)
                file.write(line)
            file.write('};\n')

    elif folder == 'p':
        routes_file = os.path.join(
            base_path, "src/routes.js")
        pages = get_all_pages()

        with open(routes_file, "r") as file:
            contents = file.readlines()
            saved = get_routes(contents)

        with open(routes_file, "w") as file:
            file.write('import React from "react";\n')
            file.write(
                'import { BrowserRouter, Route, Switch } from "react-router-dom";\n')
            for page in pages:
                line = 'import {} from "./pages/{}";\n'.format(page, page)
                file.write(line)
            file.write('\n')
            file.writelines(saved)


def get_routes(contents):
    for idx, line in enumerate(contents):
        if line.strip().startswith("class"):
            return contents[idx:]


main()
