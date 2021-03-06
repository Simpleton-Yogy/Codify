import React from 'react';
import ReactDOM from 'react-dom';
import './postPointFixed.scss';

class PostPointFixed extends React.Component {

    constructor(props){
        super(props)

    }


    render(){
        return(
            <div className="postPointFixedWrapper">
                <div className="postPointFixedTitle">{this.props.title}</div>
                <div className="postPointFixedText">{this.props.text}</div>
                <a className = "dest" href = {"/profile/" + this.props.author}><div className="postPointFixedAuthorWrapper">
                    <div className="postPointFixedCircle" />
                    <div className="postPointFixedTextWrapper">
                        <div className="postPointFixedAuthorName">{this.props.author}</div>
                        <div className="postPointFixedTime">{this.props.time}</div>
                    </div>
                </div></a>
            </div>
        )
    }

}
export default PostPointFixed;