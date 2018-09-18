import { fork, all } from "redux-saga/effects";
// import { saga as headerSaga } from "../components/Header/store";

function* rootSaga(config) {
  yield all([
    // fork(headerSaga)
  ]);
}

export default rootSaga;
