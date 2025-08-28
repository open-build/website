// Google Apps Script for Open Build website form submissions
// Deploy this as a web app and use the URL in main.js

function doPost(e) {
  try {
    let data, sheetName, formData;
    
    // Handle both JSON and FormData submissions
    if (e.postData.type === 'application/json') {
      // JSON submission
      const jsonData = JSON.parse(e.postData.contents);
      sheetName = jsonData.sheetName;
      formData = jsonData.data;
    } else {
      // FormData submission
      const params = e.parameter;
      sheetName = params.sheetName;
      formData = JSON.parse(params.data);
    }
    
    // Open the spreadsheet
    const spreadsheet = SpreadsheetApp.openById('1Zu_Ij0vG8Q_ebdjdeFVGY8cDaqyrKIXMoY9qwsgY3JM');
    
    // Get or create the sheet
    let sheet = spreadsheet.getSheetByName(sheetName);
    if (!sheet) {
      sheet = spreadsheet.insertSheet(sheetName);
      
      // Add headers based on sheet type
      if (sheetName === 'contacts') {
        sheet.getRange(1, 1, 1, 7).setValues([[
          'Timestamp', 'Name', 'Email', 'Subject', 'Message', 'Source', 'Status'
        ]]);
      } else if (sheetName === 'applications') {
        sheet.getRange(1, 1, 1, 9).setValues([[
          'Timestamp', 'Type', 'Name', 'Email', 'Experience', 'Skills', 'Motivation', 'GitHub', 'Status'
        ]]);
      }
      
      // Format header row
      const headerRange = sheet.getRange(1, 1, 1, sheet.getLastColumn());
      headerRange.setFontWeight('bold');
      headerRange.setBackground('#4285f4');
      headerRange.setFontColor('white');
    }
    
    // Prepare row data based on sheet type
    let rowData;
    if (sheetName === 'contacts') {
      rowData = [
        formData.timestamp,
        formData.name,
        formData.email,
        formData.subject,
        formData.message,
        formData.source || 'website',
        'New'
      ];
    } else if (sheetName === 'applications') {
      rowData = [
        formData.timestamp,
        formData.type,
        formData.name,
        formData.email,
        formData.experience,
        formData.skills,
        formData.motivation,
        formData.github || '',
        'New'
      ];
    }
    
    // Add the row
    sheet.appendRow(rowData);
    
    // Auto-resize columns
    sheet.autoResizeColumns(1, sheet.getLastColumn());
    
    // Send email notification (optional)
    sendEmailNotification(sheetName, formData);
    
    return ContentService
      .createTextOutput(JSON.stringify({
        success: true,
        message: 'Data submitted successfully'
      }))
      .setMimeType(ContentService.MimeType.JSON)
      .setHeaders({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
      });
      
  } catch (error) {
    console.error('Error:', error);
    return ContentService
      .createTextOutput(JSON.stringify({
        success: false,
        error: error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON)
      .setHeaders({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
      });
  }
}

function doGet(e) {
  try {
    const params = e.parameter;
    
    // Handle JSONP callback requests
    if (params.callback && params.sheetName && params.data) {
      const sheetName = params.sheetName;
      const formData = JSON.parse(params.data);
      
      // Open the spreadsheet
      const spreadsheet = SpreadsheetApp.openById('1Zu_Ij0vG8Q_ebdjdeFVGY8cDaqyrKIXMoY9qwsgY3JM');
      
      // Get or create the sheet
      let sheet = spreadsheet.getSheetByName(sheetName);
      if (!sheet) {
        sheet = spreadsheet.insertSheet(sheetName);
        
        // Add headers based on sheet type
        if (sheetName === 'contacts') {
          sheet.getRange(1, 1, 1, 7).setValues([[
            'Timestamp', 'Name', 'Email', 'Subject', 'Message', 'Source', 'Status'
          ]]);
        } else if (sheetName === 'applications') {
          sheet.getRange(1, 1, 1, 9).setValues([[
            'Timestamp', 'Type', 'Name', 'Email', 'Experience', 'Skills', 'Motivation', 'GitHub', 'Status'
          ]]);
        }
        
        // Format header row
        const headerRange = sheet.getRange(1, 1, 1, sheet.getLastColumn());
        headerRange.setFontWeight('bold');
        headerRange.setBackground('#4285f4');
        headerRange.setFontColor('white');
      }
      
      // Prepare row data based on sheet type
      let rowData;
      if (sheetName === 'contacts') {
        rowData = [
          formData.timestamp,
          formData.name,
          formData.email,
          formData.subject,
          formData.message,
          formData.source || 'website',
          'New'
        ];
      } else if (sheetName === 'applications') {
        rowData = [
          formData.timestamp,
          formData.type,
          formData.name,
          formData.email,
          formData.experience,
          formData.skills,
          formData.motivation,
          formData.github || '',
          'New'
        ];
      }
      
      // Add the row
      sheet.appendRow(rowData);
      
      // Auto-resize columns
      sheet.autoResizeColumns(1, sheet.getLastColumn());
      
      // Send email notification
      sendEmailNotification(sheetName, formData);
      
      // Return JSONP response
      const response = {
        success: true,
        message: 'Data submitted successfully'
      };
      
      return ContentService
        .createTextOutput(`${params.callback}(${JSON.stringify(response)})`)
        .setMimeType(ContentService.MimeType.JAVASCRIPT);
    }
    
    // Regular GET request
    return ContentService
      .createTextOutput(JSON.stringify({
        message: 'Open Build Form Handler is running'
      }))
      .setMimeType(ContentService.MimeType.JSON)
      .setHeaders({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
      });
      
  } catch (error) {
    console.error('Error in doGet:', error);
    
    if (e.parameter.callback) {
      // Return JSONP error response
      const response = {
        success: false,
        error: error.toString()
      };
      
      return ContentService
        .createTextOutput(`${e.parameter.callback}(${JSON.stringify(response)})`)
        .setMimeType(ContentService.MimeType.JAVASCRIPT);
    }
    
    // Return regular error response
    return ContentService
      .createTextOutput(JSON.stringify({
        success: false,
        error: error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON)
      .setHeaders({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
      });
  }
}

function doOptions(e) {
  return ContentService
    .createTextOutput('')
    .setHeaders({
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    });
}

function sendEmailNotification(sheetName, formData) {
  try {
    const recipients = 'contact@open.build'; // Change to your email
    let subject = '';
    let body = '';
    
    if (sheetName === 'contacts') {
      subject = `New Contact Form Submission - ${formData.subject}`;
      body = `
        New contact form submission received:
        
        Name: ${formData.name}
        Email: ${formData.email}
        Subject: ${formData.subject}
        Message: ${formData.message}
        
        Submitted at: ${formData.timestamp}
        Source: ${formData.source}
      `;
    } else if (sheetName === 'applications') {
      subject = `New ${formData.type} Application - ${formData.name}`;
      body = `
        New application received:
        
        Type: ${formData.type}
        Name: ${formData.name}
        Email: ${formData.email}
        Experience: ${formData.experience}
        Skills: ${formData.skills}
        Motivation: ${formData.motivation}
        GitHub: ${formData.github}
        
        Submitted at: ${formData.timestamp}
      `;
    }
    
    MailApp.sendEmail({
      to: recipients,
      subject: subject,
      body: body
    });
    
  } catch (error) {
    console.error('Error sending email notification:', error);
  }
}

// Function to set up triggers (run once)
function setupTriggers() {
  // Delete existing triggers
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));
  
  // You can add time-based triggers here if needed
  // For example, to send daily summaries:
  // ScriptApp.newTrigger('sendDailySummary')
  //   .timeBased()
  //   .everyDays(1)
  //   .atHour(9)
  //   .create();
}

// Optional: Function to send daily summary
function sendDailySummary() {
  try {
    const spreadsheet = SpreadsheetApp.openById('1Zu_Ij0vG8Q_ebdjdeFVGY8cDaqyrKIXMoY9qwsgY3JM');
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    
    let summary = 'Daily Summary for ' + Utilities.formatDate(yesterday, 'GMT', 'yyyy-MM-dd') + '\n\n';
    
    // Count new submissions
    const sheets = ['contacts', 'applications'];
    let totalSubmissions = 0;
    
    sheets.forEach(sheetName => {
      const sheet = spreadsheet.getSheetByName(sheetName);
      if (sheet) {
        const data = sheet.getDataRange().getValues();
        const newEntries = data.filter(row => {
          const timestamp = new Date(row[0]);
          return timestamp.toDateString() === yesterday.toDateString();
        });
        
        summary += `${sheetName}: ${newEntries.length} new submissions\n`;
        totalSubmissions += newEntries.length;
      }
    });
    
    if (totalSubmissions > 0) {
      MailApp.sendEmail({
        to: 'contact@open.build',
        subject: 'Open Build - Daily Summary',
        body: summary
      });
    }
    
  } catch (error) {
    console.error('Error sending daily summary:', error);
  }
}

// Helper function to format data for Slack/Discord webhooks (optional)
function sendToSlack(sheetName, formData) {
  const webhookUrl = 'YOUR_SLACK_WEBHOOK_URL';
  
  if (!webhookUrl || webhookUrl === 'YOUR_SLACK_WEBHOOK_URL') {
    return; // Skip if not configured
  }
  
  let message = '';
  if (sheetName === 'contacts') {
    message = `🆕 New contact form submission from *${formData.name}* (${formData.email})\nSubject: ${formData.subject}`;
  } else if (sheetName === 'applications') {
    message = `🎯 New ${formData.type} application from *${formData.name}* (${formData.email})\nExperience: ${formData.experience}`;
  }
  
  const payload = {
    text: message,
    username: 'Open Build Bot',
    icon_emoji: ':computer:'
  };
  
  try {
    UrlFetchApp.fetch(webhookUrl, {
      method: 'POST',
      contentType: 'application/json',
      payload: JSON.stringify(payload)
    });
  } catch (error) {
    console.error('Error sending to Slack:', error);
  }
}
