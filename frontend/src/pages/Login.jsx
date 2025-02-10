import React from "react"
import axios from 'axios'
import useSignIn from 'react-auth-kit/hooks/useSignIn';

const SignInComponent = () => {
    const signIn = useSignIn()
    const [formData, setFormData] = React.useState({email: '', password: ''})

    const onSubmit = (e) => {
        e.preventDefault()
        axios.post('/api/login', formData)
            .then((res)=>{
                if(res.status === 200){
                    if(signIn({
                        auth: {
                            token: res.data.token,
                            type: 'Bearer'
                        },
                        refresh: res.data.refreshToken,
                        userState: res.data.authUserState
                    })){ // Only if you are using refreshToken feature
                        // Redirect or do-something
                    }else {
                        //Throw error
                    }
                }
            })
    }

    return (
        <form onSubmit={onSubmit}>
            <input type={"email"} onChange={(e)=>setFormData({...formData, email: e.target.value})}/>
            <input type={"password"} onChange={(e)=>setFormData({...formData, password: e.target.value})}/>

            <button>Submit</button>
        </form>
    )
}