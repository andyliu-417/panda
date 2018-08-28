import { combineReducers } from "redux";
import { reducer as headerReducer } from "../components/Header/store";

export default combineReducers({
  header: headerReducer
});
