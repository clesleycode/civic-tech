## Technical Issues

1. Forms not updating with inserted data. 

The website has the option to create a profile, event, tech talk, etc. For the options with a foreign key, the dropdown box was not updated because of how the module works. To get around this, we consulted StackOverflow [here](https://stackoverflow.com/questions/31619747/dynamic-select-field-using-wtforms-not-updating). This allowed our website to be dynamic. 


## Technical Choices

1. Displaying our Data

Many of our pages display the current contents of our database tables. To accomplish this, we used pandas to output HTML that we then embedded into our website. This made our lives easier so we didn't have to do any iteration. Instead, this was a much more elegant solution. 

