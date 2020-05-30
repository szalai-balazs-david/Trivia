import React, { Component } from 'react';
import '../stylesheets/Question.css';

class User extends Component {
  constructor(){
    super();
  }

  render() {
    const { name, answer_count, correct_answers } = this.props;
    return (
      <div className="Question-holder">
        <div className="Question">{name}</div>
        <div className="Question-status">
          <div className="difficulty">Scores: {correct_answers} / {answer_count} good answers</div>
        </div>
      </div>
    );
  }
}

export default User;
