import * as actionTypes from "./actionType";
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

