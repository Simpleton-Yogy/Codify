import React from 'react';
import axios from 'axios';
import './LoginForm.scss';
import Button from '../Button/Button'

class LoginForm extends React.Component{

    constructor(props) {
        super(props);
        this.state = {loginStyle: {"border-color": "none"}, passwordStyle: {"border-color": "none"}, nickname: "", password: ""};
        this.setNickname = this.setNickname.bind(this);
        this.setPassword = this.setPassword.bind(this);
        this.sendData = this.sendData.bind(this)
      }

    setNickname(e){
        this.setState({nickname: e.target.value});
    }

    setPassword(e){
        this.setState({password: e.target.value});
    }

    sendData(){
        console.log(this.state.nickname + " " + this.state.password)

        let data = {nickname: this.state.nickname, password: this.state.password}

        axios.post('/loginppost', data)
             .then(response => {
                console.log(response); console.log(response.data)
        })
    }

    render(){
        return(
            <div className = "frame">
                <div className = "big-wrapper">
                    <img src = {require('../resources/ProfileIconSmall.svg')} alt = "Icon for Log in form" />
                    <form>
                        <label for = "nickname">
                            Nickname or email
                        </label>
                        <input type = "text" id = "nickname" style = {this.state.loginStyle} onChange = {this.setNickname} />
                        <label for = "password">
                            Password
                        </label>
                        <input type = "password" id = "password" style = {this.state.passwordStyle} onChange = {this.setPassword} />

                    </form>
                </div>
                <div className = "button-wrapper">
                    <Button text = "Log in" onClick = {this.sendData}/>
                </div>
            </div>
        );
    }
}

export default LoginForm;