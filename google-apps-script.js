// Google Apps Script for Open Build website form submissions
// Deploy this as a web app and use the URL in main.js

function doPost(e) {
  try {
    console.log('=== doPost START ===');
    console.log('Full event object:', JSON.stringify(e, null, 2));

    // Check if event object exists
    if (!e) {
      console.error('CRITICAL: Event object is completely undefined');
      return ContentService
        .createTextOutput(JSON.stringify({
          success: false,
          error: 'Event object is undefined - check script deployment'
        }))
        .setMimeType(ContentService.MimeType.JSON)
        .setHeaders({
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With'
        });
    }

    console.log('Event exists, checking postData...');

    // Check if postData exists
    if (!e.postData) {
      console.error('CRITICAL: postData is undefined');
      console.log('Available event properties:', Object.keys(e));
      return ContentService
        .createTextOutput(JSON.stringify({
          success: false,
          error: 'No postData received - check request format'
        }))
        .setMimeType(ContentService.MimeType.JSON)
        .setHeaders({
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With'
        });
    }

    console.log('postData exists, checking contents...');

    // Check if contents exists
    if (!e.postData.contents) {
      console.error('CRITICAL: postData.contents is undefined or empty');
      console.log('postData object:', e.postData);
      return ContentService
        .createTextOutput(JSON.stringify({
          success: false,
          error: 'No content in postData - check request body'
        }))
        .setMimeType(ContentService.MimeType.JSON)
        .setHeaders({
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With'
        });
    }

    console.log('Contents exists, parsing JSON...');
    console.log('Raw contents:', e.postData.contents);

    // Parse the request
    let data;
    try {
      data = JSON.parse(e.postData.contents);
      console.log('Parsed data:', data);
    } catch (parseError) {
      console.error('JSON parse error:', parseError);
      return ContentService
        .createTextOutput(JSON.stringify({
          success: false,
          error: 'Invalid JSON in request body: ' + parseError.toString()
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    const sheetName = data.sheetName;
    const formData = data.data;

    // Validate required fields
    if (!sheetName || !formData) {
      console.error('Missing required fields:', { sheetName, formData });
      return ContentService
        .createTextOutput(JSON.stringify({
          success: false,
          error: 'Missing sheetName or formData. Received: ' + JSON.stringify(data)
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // Open the spreadsheet
    console.log('Opening spreadsheet...');
    const spreadsheet = SpreadsheetApp.openById('1Zu_Ij0vG8Q_ebdjdeFVGY8cDaqyrKIXMoY9qwsgY3JM');
    console.log('Spreadsheet opened successfully');

    // Get or create the sheet
    console.log('Getting/creating sheet:', sheetName);
    let sheet = spreadsheet.getSheetByName(sheetName);
    if (!sheet) {
      console.log('Sheet does not exist, creating new sheet');
      sheet = spreadsheet.insertSheet(sheetName);
      console.log('New sheet created');

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
    } else {
      console.log('Existing sheet found');
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

    // Return success response
    return ContentService
      .createTextOutput(JSON.stringify({
        success: true,
        message: 'Data submitted successfully'
      }))
      .setMimeType(ContentService.MimeType.JSON)
      .setHeaders({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With'
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
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With'
      });
  }
}

function doGet(e) {
  try {
    console.log('=== doGet START ===');
    console.log('doGet called with event:', e);
    console.log('Event type:', typeof e);

    const params = e ? e.parameter : {};
    console.log('Parameters:', params);

    // Simple health check
    if (params.health === 'check') {
      return ContentService
        .createTextOutput(JSON.stringify({
          success: true,
          message: 'Google Apps Script is healthy',
          timestamp: new Date().toISOString(),
          version: '2.0',
          functions: ['doPost', 'doGet', 'doOptions']
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // If test parameter is provided, return a simple test response
    if (params.test === 'true') {
      return ContentService
        .createTextOutput(JSON.stringify({
          success: true,
          message: 'Test successful',
          timestamp: new Date().toISOString(),
          spreadsheetId: '1Zu_Ij0vG8Q_ebdjdeFVGY8cDaqyrKIXMoY9qwsgY3JM'
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    return ContentService
      .createTextOutput(JSON.stringify({
        success: true,
        message: 'Open Build Form Handler is running',
        timestamp: new Date().toISOString(),
        method: 'GET',
        parameters: params,
        instructions: 'Use ?test=true for testing or ?health=check for health check'
      }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    console.error('doGet error:', error);
    return ContentService
      .createTextOutput(JSON.stringify({
        success: false,
        error: 'doGet error: ' + error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doOptions(e) {
  try {
    console.log('=== doOptions START ===');
    console.log('doOptions called with event:', e);
    console.log('Handling CORS preflight request');

    // Handle CORS preflight requests
    return ContentService
      .createTextOutput('')
      .setMimeType(ContentService.MimeType.TEXT)
      .setHeaders({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With',
        'Access-Control-Max-Age': '86400'
      });
  } catch (error) {
    console.error('doOptions error:', error);
    return ContentService
      .createTextOutput('')
      .setMimeType(ContentService.MimeType.TEXT)
      .setHeaders({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With'
      });
  }
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
