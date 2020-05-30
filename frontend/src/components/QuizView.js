import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/QuizView.css';

const questionsPerPlay = 5; 

class QuizView extends Component {
  constructor(props){
    super();
    this.state = {
        quizCategory: null,
        previousQuestions: [], 
        showAnswer: false,
        categories: [],
        users: [],
        numCorrect: 0,
        currentQuestion: {},
        guess: '',
        user_id: null,
        forceEnd: false
    }
  }

  componentDidMount(){
    $.ajax({
      url: `/categories`,
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.message })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
    $.ajax({
      url: `/users`,
      type: "GET",
      success: (result) => {
        this.setState({ users: result.message })
        return;
      },
      error: (error) => {
        alert('Unable to load users. Please try your request again')
        return;
      }
    })
  }

  selectCategory = (type='all') => {
    this.setState({quizCategory: type}, () => this.renderSelectUser());
  }

  selectCategoryAll = () => {
    this.setState({quizCategory: 'all'}, () => this.renderSelectUser());
  }

  selectUser = (id=-1) => {
    this.setState({user_id: id}, () => this.getNextQuestion());
  }

  selectUserNone = () => {
    this.setState({user_id: -1}, () => this.getNextQuestion());
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  getNextQuestion = () => {
    const previousQuestions = [...this.state.previousQuestions]
    if(this.state.currentQuestion.id) { previousQuestions.push(this.state.currentQuestion.id) }

    $.ajax({
      url: '/',
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        previous_questions: previousQuestions,
        category: this.state.quizCategory
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          showAnswer: false,
          previousQuestions: previousQuestions,
          currentQuestion: result.message,
          guess: '',
          forceEnd: result.message ? false : true
        })
        return;
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again')
        return;
      }
    })
  }

  submitGuess = (event) => {
    event.preventDefault();
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    let evaluate =  this.evaluateAnswer()
    $.ajax({
      url: `/results`,
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({user_id: this.state.user_id, question_id: this.state.currentQuestion.id, success: evaluate}),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        return;
      },
      error: (error) => {
      //Do nothing. No point in disturbing game experience by this.
        return;
      }
    })
    this.setState({
      numCorrect: !evaluate ? this.state.numCorrect : this.state.numCorrect + 1,
      showAnswer: true,
    })
  }

  restartGame = () => {
    this.setState({
      quizCategory: null,
      previousQuestions: [], 
      showAnswer: false,
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false
    })
  }

  renderSelectUser(){
      return (
          <div className="quiz-play-holder">
              <div className="choose-header">Choose User</div>
              <div className="category-holder">
                  <div className="play-category" onClick={this.selectUserNone}>None</div>
                  {this.state.users.map((user, id) => {
                  return (
                    <div
                      key={user.name}
                      value={user.name}
                      className="play-category"
                      onClick={() => this.selectUser(user.id)}>
                      {user.name}
                    </div>
                  )
                })}
              </div>
          </div>
      )
  }

  renderPrePlay(){
      return (
          <div className="quiz-play-holder">
              <div className="choose-header">Choose Category</div>
              <div className="category-holder">
                  <div className="play-category" onClick={this.selectCategoryAll}>ALL</div>
                  {this.state.categories.map((name, ) => {
                  return (
                    <div
                      key={name}
                      value={name}
                      className="play-category"
                      onClick={() => this.selectCategory(name)}>
                      {name}
                    </div>
                  )
                })}
              </div>
          </div>
      )
  }

  renderFinalScore(){
    return(
      <div className="quiz-play-holder">
        <div className="final-header"> Your Final Score is {this.state.numCorrect}</div>
        <div className="play-again button" onClick={this.restartGame}> Play Again? </div>
      </div>
    )
  }

  evaluateAnswer = () => {
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    const answerArray = this.state.currentQuestion.answer.toLowerCase().split(' ');
    return answerArray.includes(formatGuess)
  }

  renderCorrectAnswer(){
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    let evaluate =  this.evaluateAnswer()
    return(
      <div className="quiz-play-holder">
        <div className="quiz-question">{this.state.currentQuestion.question}</div>
        <div className={`${evaluate ? 'correct' : 'wrong'}`}>{evaluate ? "You were correct!" : "You were incorrect"}</div>
        <div className="quiz-answer">Correct answer: {this.state.currentQuestion.answer}</div>
        <div className="quiz-guess">Your guess: {this.state.guess}</div>
        <div className="next-question button" onClick={this.getNextQuestion}> Next Question </div>
      </div>
    )
  }

  renderPlay(){
    return this.state.previousQuestions.length === questionsPerPlay || this.state.forceEnd
      ? this.renderFinalScore()
      : this.state.showAnswer 
        ? this.renderCorrectAnswer()
        : (
          <div className="quiz-play-holder">
            <div className="quiz-question">{this.state.currentQuestion.question}</div>
            <form onSubmit={this.submitGuess}>
              <input type="text" name="guess" onChange={this.handleChange}/>
              <input className="submit-guess button" type="submit" value="Submit Answer" />
            </form>
          </div>
        )
  }


  render() {
    return this.state.user_id
        ? this.renderPlay()
        : this.state.quizCategory
            ? this.renderSelectUser()
            : this.renderPrePlay()
  }
}

export default QuizView;
