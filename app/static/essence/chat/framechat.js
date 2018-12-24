var timeStamp = (new  Date()).getTime();
var chatClient ;
var channelType ;
var channelName ;
var myChannel ;
var memberName;
var firstTypedLetter='Y';
var endpointId ;
var flagIsPrivate ;
var configuration = null;




function getTokenAndSetupChat(memberName,endpointId)
  {
    return new Promise(function(resolve, reject)
    {

      $.get('/token?identity=' + memberName + '&endpointId=' + endpointId, function( data )
               {
                     resolve(data);
                     console.log(data);
                }
          );

    });
  }



function startChat(cobrowserId,sessionKey)
  {
       $('#chatHistory').empty();
      channelType=$('#channelType').val();
      channelName=$('#channelName').val();
      memberName=$('#memberName').val();

      if (channelName === "")
         {
            channelName="General";
         }


     if (memberName === "")
        {
            memberName = "anonymous"+timeStamp;
        }

     endpointId = memberName+':'+timeStamp;

      getTokenAndSetupChat(memberName,endpointId)
      .then(
              function(data)
                    {

                        console.log(data.token)
                        chatClient = new Twilio.Chat.Client(data.token);

	                      chatClient.initialize()
  	                       .then(function(client)
                                {

    	                            console.log("Ready to Chat , will check if channel " +channelName  + " already exists ") ;

                                  client.getChannelByUniqueName(channelName)
                                       .then(function(chosenChannel)
                                                {


                                                      myChannel.join().then(function(channel)
                                                                    {
                                                                        getFrameToWork(chosenChannel);
                                                                    });
                                                }

                                            )
                                       .catch(function(err)
                                                         {
                                                           console.log("channelType : " + channelType);
                                                           if ( channelType === "1")
                                                              {
                                                                flagIsPrivate = false ;
                                                              }
                                                          else
                                                             {
                                                               flagIsPrivate = true ;
                                                             }

                                                           console.log(channelName  + " does not exists .Will create your channel now ( private = " + flagIsPrivate + ")" ) ;

                                                           client.createChannel({
                                                                      uniqueName: channelName,
                                                                      friendlyName: channelName,
                                                                      isPrivate	: flagIsPrivate
                                                                  }).then(function(createdChannel)
                                                                  {

                                                                      createdChannel.join().then(function(channel)
                                                                                    {
                                                                                        getFrameToWork(createdChannel);
                                                                                    });
                                                           });
                                                         }

                                              )


                                  }

  	                              );



                    }
            );


  }



function getFrameToWork(channel)
{

        var clientUI = new TwilioUI.ChatUI(chatClient);
  console.log(chatClient);
        clientUI.globalization().setString('InputPlaceHolder', 'Type here like a boss (override)', 'en-GB');
        clientUI.initChannel("#chatWindow", channel, configuration);
       //clientUI.initChannel("#chatWindow", channel);
}




function showChatWindow()
  {
    $('#chatWindow').show();

  }


  function showSignInWindow()
  {
    $('#signInWindow').show();

  }


  function hideChatWindow()
  {
    $('#chatWindow').hide();

  }


  function hideSignInWindow()
  {
    $('#signInWindow').hide();

  }
