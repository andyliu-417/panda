import { put, takeEvery, all, call } from "redux-saga/effects";
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

