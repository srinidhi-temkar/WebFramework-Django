<?php

$user="root";
$pass="";
$db="testlogin";
$conn=mysqli_connect("localhost",$user,$pass,$db) or die("unable to connect");
//echo "connected";
if($_SERVER['REQUEST_METHOD']=="POST")
{
      $name=mysqli_real_escape_string($conn,$_POST['username']);
        $psd=md5($_POST['password']);
    
}

if(isset($name) && isset($psd) && !empty($name) && !empty($psd))
{
$sql = "SELECT Username, Password FROM users";
$check=mysqli_query($conn,$sql);
$flag=0;
if (mysqli_num_rows($check) > 0)
{
    $spsd=substr($psd,0,10);
    //echo $name;
    //echo $spsd;
    while($row=mysqli_fetch_assoc($check))
    {
    $check_username=$row['Username'];
    $check_password=$row['Password'];
    if($name == $check_username && $spsd == $check_password){
            $flag=1;
            break;
        }

    }
    
   if($flag==1)
   {
       echo "<script>window.location = 'profile.html'</script>";
   } 
   else
   {
        echo "<script>
            alert('The entered username or password does not exist.Please enter your details again.');
            window.location.href='login.php'</script>";
        unset($name);
        unset($psd);
   }
}
}
mysqli_close($conn);
?>

<!DOCTYPE html>
<html>
    <head>
    </head>
    <style>
    body{
        background-image: url('images/bg3.jpg');
        background-repeat: no-repeat;
        background-size: 100% ;
        }
    input[type=text],
    input[type=password] {
    padding: 12px 10px;
    margin: 5px 0;
    display: flex;
    border: 1px solid #ccc;
    box-sizing: border-box;
    
    }
    .login{
    width:400px;
    height:450px;
    background:white;
    color:black;
    top:50%;
    left:50%;
    position: absolute;
    transform: translate(-50%,-50%);
    box-sizing: border-box;
    padding: 70px 30px;
    border-radius: 16px;
    }
   
    #up{
        
        font-family: Arial, sans-serif;
        font-size:20px;
    }
    .head{
        
        font-family:'Franklin Gothic Medium',Arial, sans-serif;
        font-size:35px;
        text-align: center;
    }
    body{
        background-color:peachpuff;
    }
    .button{
        background-color: palevioletred;
        text-align: center;
        padding: 14px 10px;
        margin: 8px 10px;
        border: none;
        cursor: pointer;
        width: 43.5%;
        border-radius: 18px;
    }
     a{
        display: inline-block;
        font-family:Arial, sans-serif;
        font-size: 13.5px;
        line-height: 15px;
        color:darkgray;
        
        }
    a:hover{
    color:black;
    }   


    
</style>

    <body>
        <div class="login">
             <form action="login.php" method="post">
                <div class="container">
                    <div class="head"><label id="head1">Welcome Back </label></div><br><br>
                    <label id="up" ><b>Username</b></label><br>
                        <input type="text" name="username" placeholder="Enter Username" size="43"  required>
                            <br>
                        <label id="up"><b>Password</b></label><br>
                            <input type="password" name="password" placeholder="Enter Password" size="43" maxlength="10" required>
                            <br>
                            
                        <button type="submit" class="button" onclick ="getProfile()">Login</button>
                        <button type="button" class="button" onclick="back()">Cancel</button><br>
                        <a href="#"  style=" padding-left: 105px;" >Forgot password?</a><br>
                        <a href="#" style="padding-left: 95px" onclick="location.href='signup.php'">Don't have an account</a>
                </div>
            </form>
        </div>
        <script>
            function back()
            {
               var check= confirm("Are you sure?");
               if(check == true)
                    return location.href='index.html';
            

            }
            function getProfile(){
                //code for validity
                if(form.password.value=="" || form.user.value=="")
                {
                    alert("Please fill the field");
                    return false;
                }
                return location.href="mikeross.html";
            }
        </script>
    </body>
</html>

