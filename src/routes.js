import React from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom";
// import Home from "./pages/Home";

class Routes extends React.Component {
  render() {
    return (
      <BrowserRouter>
        <Switch>
          {/* <Route path="/" exact component={Home} /> */}
        </Switch>
      </BrowserRouter>
    );
  }
}

export default Routes;
