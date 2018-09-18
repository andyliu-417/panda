import sys
import os
import shutil

pages = []
components = []
REMOVE_FILES = ['.gitignore', '.zshrc', 'scripts.py', '.git', 'test_scripts']
isNew = False

def copytree(src, dst):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)


def handle_parameters():
    global isNew
    if sys.argv[2] == 'new':
        isNew = True
        global PROJECT_PATH, PANDA_PATH
        PROJECT_PATH = os.path.join(sys.argv[1], sys.argv[3])
        PANDA_PATH = "/Users/andy/repos/panda"
        print(PANDA_PATH)
        os.mkdir(PROJECT_PATH)
        copytree(PANDA_PATH, PROJECT_PATH)
        for file in REMOVE_FILES:
            file_path = os.path.join(PROJECT_PATH, file)
            os.path.exists(file_path) and os.remove(file_path) if os.path.isfile(file_path) else shutil.rmtree(file_path)

    else:
        global base_path, SRC_PATH, COMBINE_STORE_PATH, PAGES_PATH, COMPONENTS_PATH, v, o, page_name, component_name, cp_name, class_name, class_file_name, style_name, tag_name
        base_path = sys.argv[1]
        SRC_PATH = os.path.join(base_path, 'src')
        COMBINE_STORE_PATH = os.path.join(SRC_PATH, 'store')
        PAGES_PATH = os.path.join(SRC_PATH, 'pages')
        COMPONENTS_PATH = os.path.join(SRC_PATH, 'components')

        v = sys.argv[2][0]
        o = sys.argv[2][-1]
        cp = sys.argv[3]
        (page_name, component_name) = extract_page_component(cp)
        cp_name = page_name if page_name else component_name
        class_name = component_name if component_name else page_name
        class_file_name = "index" if cp_name == class_name else class_name
        if len(sys.argv) > 4:
            s = sys.argv[4]
            style_name = (
                component_name if component_name else page_name) + s.capitalize()
            tag_name = sys.argv[5]

        print("starting to create {}/{}...".format(cp_name, class_name))


def extract_page_component(cp):
    index = cp.find(':')
    if index > -1:
        return (cp[:index].capitalize(), cp[index+1:].capitalize())
    elif o == 'p':
        return (cp.capitalize(), "")
    elif o == 'c':
        return ("", cp.capitalize())
    elif o == 's':
        get_all_pages()
        if cp.capitalize() in pages:
            return (cp.capitalize(), "")
        get_all_components()
        if cp.capitalize() in components:
            return ("", cp.capitalize())


def handle_paths():
    global CP_PATH, STORE_PATH
    if page_name:
        CP_PATH = os.path.join(PAGES_PATH, page_name)
    else:
        CP_PATH = os.path.join(COMPONENTS_PATH, component_name)
    STORE_PATH = os.path.join(CP_PATH, 'store')


def get_all_stores():
    get_all_pages()
    get_all_components()
    return pages + components


def get_all_pages():
    for page in os.listdir(PAGES_PATH):
        if os.path.isdir(os.path.join(PAGES_PATH, page)):
            pages.append(page)


def get_all_components():
    for component in os.listdir(COMPONENTS_PATH):
        if os.path.isdir(os.path.join(COMPONENTS_PATH, component)):
            components.append(component)


def generate_style():
    style_path = os.path.join(CP_PATH, "style.js")
    style(style_path)


def style(style_path):
    with open(style_path, "a") as file:
        template = '''export const {style_name} = styled.{tag_name}`\n
`;\n\n'''
        context = {
            "style_name": style_name,
            "tag_name": tag_name
        }
        file.write(template.format(**context))

    styles = get_styles(style_path)

    file_path = os.path.join(CP_PATH, class_file_name + ".js")
    contents = []
    with open(file_path, "r") as file:
        contents = file.readlines()

    style_line = ''
    for idx, line in enumerate(contents):
        if "./style" in line.strip():
            if line.strip().startswith('import'):
                style_line = 'import { '
                style_line += ', '.join(styles)
                style_line += ' } from "./style";\n'
                contents[idx] = style_line
            else:
                contents[idx-1] = contents[idx-1][:-1]+',\n'
                contents.insert(idx, '  '+styles[-1]+',\n')
            break

    with open(file_path, "w") as file:
        file.writelines(contents)


def get_styles(style_path):
    styles = []

    with open(style_path, "r") as file:
        contents = file.readlines()
    for line in contents:
        if line.strip().startswith("export") and class_name in line.strip():
            words = line.split(' ')
            styles.append(words[2])
    return styles


def handle_generate():
    if o == 'p':
        generate_page()
        print("created page {} successfully".format(class_name))
    elif o == 'c':
        generate_component()
        print("created component {} successfully".format(class_name))
    elif o == 's':
        generate_style()
        print("created {} successfully".format(style_name))


def handle_remove():
    shutil.rmtree(CP_PATH)
    update_combine_Store()
    import_routers()
    export_components()


def page_index():
    file_path = os.path.join(CP_PATH, class_file_name+".js")
    template = """import React, {{ PureComponent }} from "react";
import {{ connect }}from "react-redux";
import {{ actionCreators, selectors }} from "./store";
import {{ }} from "./style";

class {class_name} extends PureComponent {{
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
    print("index in {} is created successfully.".format(class_name))


def page_style():
    file_path = os.path.join(CP_PATH, "style.js")
    content = 'import styled from "styled-components";\n\n'
    with open(file_path, "w") as file:
        file.write(content)
    print("style in {} is created successfully.".format(class_name))


def store_index():
    file_path = os.path.join(STORE_PATH, "index.js")

    template = """import reducer from "./reducer";
import saga from "./saga";
import * as actionCreators from "./actionCreator";
import * as actionTypes from "./actionType";
import * as selectors from './selectors';

export { reducer, saga, actionCreators, actionTypes, selectors };

"""
    with open(file_path, "w") as file:
        file.write(template)


def store_reducer():
    file_path = os.path.join(STORE_PATH, "reducer.js")

    template = """import * as actionTypes from "./actionType";
import { fromJS } from "immutable";

const defaultState = fromJS({
  // foo: "foo",
});

const reducer_handlers = {
  // [actionTypes.FOO]: (state, action) => {
  //   return state.set("key", val);
  // }
};

export default (state = defaultState, action) => {
  if (reducer_handlers.hasOwnProperty(action.type)) {
    console.log("reducer", action);
    return reducer_handlers[action.type](state, action);
  }
  return state;
};

"""
    with open(file_path, "w") as file:
        file.write(template)


def store_saga():
    file_path = os.path.join(STORE_PATH, "saga.js")

    template = """import { put, takeEvery, all, call } from "redux-saga/effects";
import * as actionTypes from "./actionType";

const saga_handlers = {
  // [actionTypes.FOO]: function*(action) {
  //   try {
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
        console.log("saga", action);
        return saga_handlers[action.type](action);
      }
    )
  ]);
}

export default saga;

"""
    with open(file_path, "w") as file:
        file.write(template)


def store_creator():
    file_path = os.path.join(STORE_PATH, "actionCreator.js")

    template = """import * as actionTypes from './actionType';

// export const foo = () => ({
//     type: actionTypes.FOO
// }); 

"""
    with open(file_path, "w") as file:
        file.write(template)


def store_type():
    file_path = os.path.join(STORE_PATH, "actionType.js")

    template = """// export const FOO = "{cp_name}_foo";
"""
    context = {
        "cp_name": cp_name.lower()
    }
    with open(file_path, "w") as file:
        file.write(template.format(**context))


def store_selector():
    file_path = os.path.join(STORE_PATH, "selectors.js")

    template = """import {{ createSelector }} from "reselect";

// const selectFoo = state => state.getIn(['{cp_name}', 'foo']);
// export const fooSelector = createSelector(selectFoo, item => item);

"""
    context = {
        "cp_name": cp_name
    }
    with open(file_path, "w") as file:
        file.write(template.format(**context))


def page_store():
    os.makedirs(STORE_PATH)

    store_index()
    store_reducer()
    store_saga()
    store_creator()
    store_type()
    store_selector()
    print("store in {} is created successfully.".format(class_name))


def generate_page():
    if not os.path.exists(CP_PATH):
        os.makedirs(CP_PATH)
        page_index()
        page_style()
        page_store()
        update_combine_Store()
        import_routers()
    else:
        print("page {} existed already.".format(class_name))


def import_index():
    index_file = os.path.join(CP_PATH, "index.js")
    (index, contents) = find_line_idx_in_file(index_file, "./style")
    line = 'import {} from "./{}"\n'.format(class_name, class_name)
    contents.insert(index+1, line)
    with open(index_file, "w") as file:
        file.writelines(contents)


def find_line_idx_in_file(file_name, keyword):
    contents = []
    with open(file_name, "r") as file:
        contents = file.readlines()
    for idx, line in enumerate(contents):
        if keyword in line.strip():
            return (idx, contents)


def generate_component():
    if not os.path.exists(CP_PATH):
        os.makedirs(CP_PATH)
        page_index()
        page_style()
        page_store()
        update_combine_Store()
        export_components()
    else:
        page_index()
        import_index()


def import_routers():
    routes_file = os.path.join(
        SRC_PATH, "routes.js")

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

    print("updated routes successfully.")


def get_routes(contents):
    for idx, line in enumerate(contents):
        if line.strip().startswith("class"):
            return contents[idx:]


def export_components():
    index_file = os.path.join(COMPONENTS_PATH, "index.js")
    with open(index_file, "w") as file:
        for component in components:
            line = 'import {} from "./{}";\n'.format(component, component)
            file.write(line)
        file.write('\n')
        file.write('export {\n')
        for component in components:
            line = '    {},\n'.format(component)
            file.write(line)
        file.write('};\n')


def update_combine_Store():
    stores = get_all_stores()
    updateCombineReducer(stores)
    updateCombineSaga(stores)
    print("updated store successfully.")


def updateCombineReducer(stores):
    reducer_file = os.path.join(COMBINE_STORE_PATH, "reducer.js")
    with open(reducer_file, "w") as file:
        file.write('import { combineReducers } from "redux-immutable";\n')
        for page in pages:
            line = 'import {{ reducer as {}Reducer }} from "../{}/{}/store"\n'.format(
                page, 'pages', page)
            file.write(line)
        for component in components:
            line = 'import {{ reducer as {}Reducer }} from "../{}/{}/store"\n'.format(
                component, 'components', component)
            file.write(line)

        file.write('\n')

        file.write('export default combineReducers({\n')
        for store in stores:
            line = '  {}: {}Reducer,\n'.format(store, store)
            file.write(line)
        file.write("});\n")


def updateCombineSaga(stores):
    saga_file = os.path.join(COMBINE_STORE_PATH, "saga.js")
    with open(saga_file, "w") as file:
        file.write('import { fork, all } from "redux-saga/effects";\n')
        for page in pages:
            line = 'import {{ saga as {}Saga }} from "../{}/{}/store"\n'.format(
                page, 'pages', page)
            file.write(line)
        for component in components:
            line = 'import {{ saga as {}Saga }} from "../{}/{}/store"\n'.format(
                component, 'components', component)
            file.write(line)
        file.write('\n')
        file.write('function* rootSaga(config) {\n')
        file.write('  yield all([\n')

        for store in stores:
            line = '    fork({}Saga),\n'.format(store)
            file.write(line)
        file.write("  ]);\n")
        file.write("}\n\n")
        file.write("export default rootSaga;\n")


def main():
    try:
        handle_parameters()
        if not isNew:
            handle_paths()
            if v == 'g':
                handle_generate()
            elif v == 'r':
                handle_remove()
    except Exception as e:
        print(e)


main()
