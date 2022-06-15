import  React,{Component } from "react";
import '../stylesheets/Custom.css'

class UserForm extends Component{
    constructor(props){
        super(props)
    }

    render(){
        return(
            <form action=""
            onSubmit={this.props.onSubmit}
             className="user-form">
                <label htmlFor="user_name">Enter your name:</label>
                <input type="text" name="user_name" id="" onChange={this.props.onHandleChange} />
                <input type="submit" value="Submit" />
            </form>
            
        );
    }
}
export default UserForm