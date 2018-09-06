import sys
import os
import shutil

tree = {}
pages = []
components = []


def handle_parameters():
    global base_path, v, o, page_name, component_name, cp_name, style_name, tag_name
    base_path = sys.argv[1]
    v = sys.argv[2][0]
    o = sys.argv[2][-1]
    cp = sys.argv[3]
    (page_name, component_name) = extract_page_component(cp)
    cp_name = page_name if page_name else component_name
    if len(sys.argv) > 4:
        s = sys.argv[4]
        style_name = (
            component_name if component_name else page_name) + s.capitalize()
        tag_name = sys.argv[5]


def extract_page_component(cp):
    index = cp.find(':')
    if index > -1:
        return (cp[:index].capitalize(), cp[index+1:].capitalize())
    elif o == 'p':
        return (cp.capitalize(), "")
    elif o == 'c':
        return ("", cp.capitalize())


def handle_paths():
    global SRC_PATH, PAGES_PATH, COMPONENTS_PATH, CP_PATH, STORE_PATH, COMBINE_STORE_PATH
    SRC_PATH = os.path.join(base_path, 'src')
    COMBINE_STORE_PATH = os.path.join(SRC_PATH, 'store')
    PAGES_PATH = os.path.join(SRC_PATH, 'pages')
    COMPONENTS_PATH = os.path.join(SRC_PATH, 'components')
    if page_name:
        CP_PATH = os.path.join(PAGES_PATH, page_name)
    else:
        CP_PATH = os.path.join(COMPONENTS_PATH, component_name)
    STORE_PATH = os.path.join(CP_PATH, 'store')

def get_all_pages():
    for page in os.listdir(PAGES_PATH):
        if os.path.isdir(os.path.join(PAGES_PATH, page)):
            pages.append(page)
    return pages


def get_all_components():
    components = []
    for component in os.listdir(COMPONENTS_PATH):
        if os.path.isdir(os.path.join(COMPONENTS_PATH, component)):
            components.append(component)
    return components


def handle_generate():
    if o == 'p':
        generate_page()
    elif o == 'c':
        pass

def page_index():
    file_path = os.path.join(CP_PATH, "index.js")
    template = """import React, {{ PureComponent }} from "react";
import {{ connect }}from "react-redux";
import {{ actionCreators, selectors }} from "./store";
import {{ }} from "./style";

class {page_name} extends PureComponent {{
  render() {{
    return <div>{page_name}</div>;
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
)({page_name});

"""

    context = {
        "page_name": page_name
    }
    with open(file_path, "w") as file:
        file.write(template.format(**context))
    print(file_path, "is successful.")

def page_style():
    file_path = os.path.join(CP_PATH, "style.js")
    content = 'import styled from "styled-components";\n\n'
    with open(file_path, "w") as file:
        file.write(content)
    print(file_path, "is successful.")

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


def store_saga():
    file_path = os.path.join(STORE_PATH, "saga.js")

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
        "cp_name": cp_name
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
    print(STORE_PATH, "is successful.")

def generate_page():
    os.makedirs(CP_PATH)
    page_index()
    page_style()
    page_store()

def makeTree():
    pass
    
handle_parameters()
handle_paths()
handle_generate()
