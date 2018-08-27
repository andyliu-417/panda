import { fork, all } from 'redux-saga/effects';

function* rootSaga(config) {
  yield all([fork()]);
}

export default rootSaga;
