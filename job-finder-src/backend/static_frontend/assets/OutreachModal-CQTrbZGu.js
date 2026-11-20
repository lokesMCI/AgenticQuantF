import{a as e,i as t,n,o as r,r as i}from"./index-3aJXrfqV.js";var a=r(e(),1),o=t(),s=n(),c=({isOpen:e,onClose:t,recruiterInfo:n,messageData:r,jobTitle:c,company:l,onSendEmail:u,onCopyToClipboard:d,anchorTop:f=0})=>{let[p,m]=(0,a.useState)(`email`),[h,g]=(0,a.useState)(null),[_,v]=(0,a.useState)({}),[y,b]=(0,a.useState)(!1),x=i(e,t);if(!e)return null;let S={why_applying:_.why_applying===void 0?r?.why_applying||``:_.why_applying,why_fit:_.why_fit===void 0?r?.why_fit||``:_.why_fit,questions:_.questions===void 0?r?.questions||[]:_.questions,email_subject:_.email_subject===void 0?r?.email_subject||``:_.email_subject,email_body:_.email_body===void 0?r?.email_body||``:_.email_body,linkedin_message:_.linkedin_message===void 0?r?.linkedin_message||``:_.linkedin_message},C=e=>{g(e)},w=(e,t)=>{v(n=>({...n,[e]:t})),g(null)},T=()=>{let e=`Subject: ${S.email_subject}\n\n${S.email_body}`;navigator.clipboard.writeText(e),b(!0),setTimeout(()=>b(!1),2e3)},E=()=>{navigator.clipboard.writeText(S.linkedin_message),b(!0),setTimeout(()=>b(!1),2e3)};return(0,o.createPortal)((0,s.jsxs)(`div`,{className:`modal-overlay`,onClick:t,style:{alignItems:`flex-start`,paddingTop:Math.max(20,f)},children:[(0,s.jsxs)(`div`,{ref:x,className:`modal-content outreach-modal`,role:`dialog`,"aria-modal":`true`,"aria-label":`Personalized Outreach`,tabIndex:-1,onClick:e=>e.stopPropagation(),children:[(0,s.jsxs)(`div`,{className:`modal-header`,children:[(0,s.jsxs)(`div`,{children:[(0,s.jsx)(`h2`,{children:`Personalized Outreach`}),(0,s.jsxs)(`p`,{className:`modal-subtitle`,children:[c,` at `,l,n?.recruiter_name&&` • ${n.recruiter_name}`]})]}),(0,s.jsx)(`button`,{className:`modal-close`,onClick:t})]}),n?.quota_exhausted?(0,s.jsxs)(`div`,{className:`recruiter-info-box`,style:{background:`rgba(234, 179, 8, 0.08)`,borderColor:`rgba(234, 179, 8, 0.3)`,display:`flex`,alignItems:`flex-start`,gap:`10px`},children:[(0,s.jsxs)(`svg`,{width:`18`,height:`18`,viewBox:`0 0 24 24`,fill:`none`,stroke:`#EAB308`,strokeWidth:`2`,strokeLinecap:`round`,strokeLinejoin:`round`,style:{flexShrink:0,marginTop:`2px`},children:[(0,s.jsx)(`path`,{d:`M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z`}),(0,s.jsx)(`line`,{x1:`12`,y1:`9`,x2:`12`,y2:`13`}),(0,s.jsx)(`line`,{x1:`12`,y1:`17`,x2:`12.01`,y2:`17`})]}),(0,s.jsxs)(`div`,{children:[(0,s.jsx)(`div`,{style:{fontSize:`0.86rem`,color:`#FDE047`,fontWeight:600,margin:`0 0 3px 0`},children:`Google Search Grounding free-tier daily quota limit reached`}),(0,s.jsx)(`div`,{style:{fontSize:`0.78rem`,color:`var(--text-muted)`,lineHeight:1.4},children:`The outreach note has been addressed to the Hiring Team. You can set a custom Gemini API Key in Settings for unlimited search grounding.`})]})]}):n?.recruiter_name?(0,s.jsxs)(`div`,{className:`recruiter-info-box`,children:[(0,s.jsx)(`div`,{className:`recruiter-name`,children:n.recruiter_name}),n?.recruiter_profile_url&&(0,s.jsx)(`a`,{href:n.recruiter_profile_url,target:`_blank`,rel:`noopener noreferrer`,className:`recruiter-link`,children:`View Profile`})]}):(0,s.jsxs)(`div`,{className:`recruiter-info-box`,style:{opacity:.85,display:`flex`,alignItems:`center`,gap:`10px`},children:[(0,s.jsxs)(`svg`,{width:`15`,height:`15`,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:`2`,strokeLinecap:`round`,strokeLinejoin:`round`,style:{color:`var(--accent-primary)`,flexShrink:0},children:[(0,s.jsx)(`circle`,{cx:`12`,cy:`12`,r:`10`}),(0,s.jsx)(`line`,{x1:`12`,y1:`16`,x2:`12`,y2:`12`}),(0,s.jsx)(`line`,{x1:`12`,y1:`8`,x2:`12.01`,y2:`8`})]}),(0,s.jsx)(`div`,{children:(0,s.jsx)(`div`,{className:`recruiter-name`,style:{fontSize:`0.86rem`,color:`var(--text-main)`,margin:0},children:`Recruiter info not detected in posting — addressed to Hiring Team`})})]}),(0,s.jsxs)(`div`,{className:`outreach-tabs`,children:[(0,s.jsx)(`button`,{className:`tab-button ${p===`email`?`active`:``}`,onClick:()=>m(`email`),children:`Email`}),(0,s.jsx)(`button`,{className:`tab-button ${p===`linkedin`?`active`:``}`,onClick:()=>m(`linkedin`),children:`LinkedIn Message`})]}),(0,s.jsxs)(`div`,{className:`outreach-content`,children:[p===`email`&&(0,s.jsxs)(`div`,{className:`email-section`,children:[(0,s.jsxs)(`div`,{className:`message-section`,children:[(0,s.jsxs)(`div`,{className:`section-header`,children:[(0,s.jsx)(`span`,{className:`section-title`,children:`Subject Line`}),(0,s.jsx)(`button`,{className:`edit-button`,onClick:()=>C(`email_subject`),children:`Edit`})]}),h===`email_subject`?(0,s.jsxs)(`div`,{className:`edit-form`,children:[(0,s.jsx)(`input`,{type:`text`,value:S.email_subject,onChange:e=>v(t=>({...t,email_subject:e.target.value})),className:`edit-input`}),(0,s.jsxs)(`div`,{className:`edit-buttons`,children:[(0,s.jsx)(`button`,{className:`btn btn-small`,onClick:()=>w(`email_subject`,S.email_subject),children:`Save`}),(0,s.jsx)(`button`,{className:`btn btn-small btn-secondary`,onClick:()=>g(null),children:`Cancel`})]})]}):(0,s.jsx)(`div`,{className:`message-text`,children:S.email_subject})]}),(0,s.jsxs)(`div`,{className:`message-section`,children:[(0,s.jsxs)(`div`,{className:`section-header`,children:[(0,s.jsx)(`span`,{className:`section-title`,children:`Email Body`}),(0,s.jsx)(`button`,{className:`edit-button`,onClick:()=>C(`email_body`),children:`Edit`})]}),h===`email_body`?(0,s.jsxs)(`div`,{className:`edit-form`,children:[(0,s.jsx)(`textarea`,{value:S.email_body,onChange:e=>v(t=>({...t,email_body:e.target.value})),className:`edit-textarea`,rows:`10`}),(0,s.jsxs)(`div`,{className:`edit-buttons`,children:[(0,s.jsx)(`button`,{className:`btn btn-small`,onClick:()=>w(`email_body`,S.email_body),children:`Save`}),(0,s.jsx)(`button`,{className:`btn btn-small btn-secondary`,onClick:()=>g(null),children:`Cancel`})]})]}):(0,s.jsx)(`div`,{className:`message-text`,style:{whiteSpace:`pre-wrap`},children:S.email_body})]}),(0,s.jsxs)(`div`,{className:`action-buttons`,style:{display:`flex`,gap:`8px`,flexWrap:`wrap`},children:[(0,s.jsx)(`button`,{className:`btn`,onClick:T,style:{flex:`1 1 auto`},children:y?`Copied!`:`Copy Email`}),(0,s.jsx)(`button`,{className:`btn btn-secondary`,onClick:()=>{let e=encodeURIComponent(S.email_subject),t=encodeURIComponent(S.email_body),r=`https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(n?.recruiter_email||``)}&su=${e}&body=${t}`;window.open(r,`_blank`),console.log(`[OutreachModal] Opened Gmail draft with:`,{to:n?.recruiter_email,subject:S.email_subject,bodyLength:S.email_body.length})},style:{flex:`1 1 auto`},title:`Opens Gmail with pre-filled draft`,"aria-label":`Opens Gmail with pre-filled draft`,children:`Open in Gmail`}),(0,s.jsx)(`button`,{className:`btn btn-secondary`,onClick:()=>{let e=encodeURIComponent(S.email_subject),t=encodeURIComponent(S.email_body),r=encodeURIComponent(n?.recruiter_email||``);window.location.href=`mailto:${r}?subject=${e}&body=${t}`},style:{flex:`1 1 auto`},title:`Opens your default mail client (Outlook, Apple Mail, etc.)`,"aria-label":`Opens your default mail client (Outlook, Apple Mail, etc.)`,children:`Open Default Mail Client`})]})]}),p===`linkedin`&&(0,s.jsx)(`div`,{className:`linkedin-section`,children:(0,s.jsxs)(`div`,{className:`message-section`,style:{background:`rgba(15, 23, 42, 0.65)`,border:`1px solid rgba(255, 255, 255, 0.08)`,borderRadius:`12px`,overflow:`hidden`},children:[(0,s.jsxs)(`div`,{className:`section-header`,style:{padding:`12px 16px`,background:`rgba(255, 255, 255, 0.02)`,borderBottom:`1px solid rgba(255, 255, 255, 0.06)`,display:`flex`,alignItems:`center`,justifyContent:`space-between`,marginBottom:0},children:[(0,s.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:`8px`},children:[(0,s.jsxs)(`svg`,{width:`15`,height:`15`,viewBox:`0 0 24 24`,fill:`none`,stroke:`#0A66C2`,strokeWidth:`2`,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,s.jsx)(`path`,{d:`M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z`}),(0,s.jsx)(`rect`,{x:`2`,y:`9`,width:`4`,height:`12`}),(0,s.jsx)(`circle`,{cx:`4`,cy:`4`,r:`2`})]}),(0,s.jsx)(`span`,{style:{fontWeight:600,color:`var(--text-main)`,fontSize:`0.88rem`},children:`LinkedIn Note / InMail`}),(0,s.jsxs)(`span`,{style:{fontSize:`0.74rem`,padding:`2px 8px`,borderRadius:`10px`,background:(S.linkedin_message||``).length<=300?`rgba(16, 185, 129, 0.12)`:`rgba(245, 158, 11, 0.12)`,color:(S.linkedin_message||``).length<=300?`#34D399`:`#FBBF24`,fontWeight:600},children:[(S.linkedin_message||``).length,` / 300 chars`]})]}),h!==`linkedin_message`&&(0,s.jsxs)(`button`,{className:`btn btn-secondary`,style:{padding:`4px 10px`,fontSize:`0.76rem`,gap:`4px`},onClick:()=>C(`linkedin_message`),children:[(0,s.jsxs)(`svg`,{width:`12`,height:`12`,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:`2`,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,s.jsx)(`path`,{d:`M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7`}),(0,s.jsx)(`path`,{d:`M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z`})]}),`Edit`]})]}),(0,s.jsx)(`div`,{style:{padding:`16px`},children:h===`linkedin_message`?(0,s.jsxs)(`div`,{className:`edit-form`,children:[(0,s.jsx)(`textarea`,{value:S.linkedin_message,onChange:e=>v(t=>({...t,linkedin_message:e.target.value})),className:`edit-textarea`,rows:`5`,style:{width:`100%`,background:`rgba(0, 0, 0, 0.3)`,border:`1px solid rgba(56, 189, 248, 0.3)`,borderRadius:`8px`,color:`var(--text-main)`,padding:`12px`,fontSize:`0.9rem`,lineHeight:1.6,resize:`vertical`}}),(0,s.jsxs)(`div`,{className:`edit-buttons`,style:{display:`flex`,gap:`8px`,justifyContent:`flex-end`,marginTop:`10px`},children:[(0,s.jsx)(`button`,{className:`btn btn-secondary`,style:{padding:`6px 14px`,fontSize:`0.8rem`},onClick:()=>g(null),children:`Cancel`}),(0,s.jsx)(`button`,{className:`btn`,style:{padding:`6px 16px`,fontSize:`0.8rem`},onClick:()=>w(`linkedin_message`,S.linkedin_message),children:`Save Changes`})]})]}):(0,s.jsx)(`div`,{style:{background:`rgba(0, 0, 0, 0.25)`,border:`1px solid rgba(255, 255, 255, 0.05)`,borderRadius:`8px`,padding:`14px 16px`,color:`var(--text-main)`,fontSize:`0.9rem`,lineHeight:1.65,whiteSpace:`pre-wrap`},children:S.linkedin_message})}),(0,s.jsxs)(`div`,{style:{padding:`12px 16px`,background:`rgba(0, 0, 0, 0.2)`,borderTop:`1px solid rgba(255, 255, 255, 0.06)`,display:`flex`,alignItems:`center`,justifyContent:`space-between`,gap:`12px`,flexWrap:`wrap`},children:[(0,s.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:`6px`,fontSize:`0.8rem`,color:`var(--text-muted)`},children:[(0,s.jsxs)(`svg`,{width:`13`,height:`13`,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:`2`,strokeLinecap:`round`,strokeLinejoin:`round`,style:{color:`var(--accent-primary)`,flexShrink:0},children:[(0,s.jsx)(`circle`,{cx:`12`,cy:`12`,r:`10`}),(0,s.jsx)(`line`,{x1:`12`,y1:`16`,x2:`12`,y2:`12`}),(0,s.jsx)(`line`,{x1:`12`,y1:`8`,x2:`12.01`,y2:`8`})]}),(0,s.jsx)(`span`,{children:`Paste into the connection request note box`})]}),(0,s.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:`8px`},children:[(0,s.jsxs)(`button`,{className:`btn`,style:{padding:`7px 16px`,fontSize:`0.82rem`,gap:`6px`,display:`inline-flex`,alignItems:`center`},onClick:E,children:[(0,s.jsxs)(`svg`,{width:`13`,height:`13`,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:`2`,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,s.jsx)(`rect`,{x:`9`,y:`9`,width:`13`,height:`13`,rx:`2`,ry:`2`}),(0,s.jsx)(`path`,{d:`M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1`})]}),y?`Copied!`:`Copy Message`]}),n?.recruiter_profile_url&&(0,s.jsxs)(`button`,{className:`btn btn-secondary`,style:{padding:`7px 16px`,fontSize:`0.82rem`,gap:`6px`,display:`inline-flex`,alignItems:`center`},onClick:()=>{E(),window.open(n.recruiter_profile_url,`_blank`)},title:`Copies note and opens recruiter profile in new tab`,children:[(0,s.jsxs)(`svg`,{width:`13`,height:`13`,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:`2`,strokeLinecap:`round`,strokeLinejoin:`round`,style:{color:`#0A66C2`},children:[(0,s.jsx)(`path`,{d:`M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6`}),(0,s.jsx)(`polyline`,{points:`15 3 21 3 21 9`}),(0,s.jsx)(`line`,{x1:`10`,y1:`14`,x2:`21`,y2:`3`})]}),`Open Profile`]})]})]})]})})]}),(0,s.jsxs)(`div`,{className:`message-sections-preview`,children:[(0,s.jsx)(`div`,{className:`section-label`,children:`Message Sections`}),(0,s.jsxs)(`div`,{className:`sections-grid`,children:[(0,s.jsxs)(`div`,{className:`section-card`,children:[(0,s.jsx)(`h4`,{children:`Why I'm Applying`}),(0,s.jsx)(`p`,{children:S.why_applying})]}),(0,s.jsxs)(`div`,{className:`section-card`,children:[(0,s.jsx)(`h4`,{children:`Why I Fit`}),(0,s.jsx)(`p`,{children:S.why_fit})]}),(0,s.jsxs)(`div`,{className:`section-card`,children:[(0,s.jsx)(`h4`,{children:`Questions`}),(0,s.jsx)(`ul`,{children:S.questions?.map((e,t)=>(0,s.jsx)(`li`,{children:e},t))})]})]})]})]}),(0,s.jsx)(`style`,{children:`
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.85);
          display: flex;
          align-items: flex-start;
          justify-content: center;
          z-index: 1000;
          padding: 40px 20px;
          overflow-y: auto;
          pointer-events: none; /* Let scroll/mouse pass to background */
        }

        .modal-content {
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: 20px;
          max-width: 1040px;
          width: 92vw;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7);
          margin-bottom: 40px;
          pointer-events: auto; /* Keep modal interactive */
        }

        .outreach-modal {
          padding: 0;
        }

        .modal-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          padding: 24px;
          border-bottom: 1px solid var(--border-color);
          gap: 16px;
        }

        .modal-header h2 {
          margin: 0 0 4px 0;
          font-size: 1.3rem;
        }

        .modal-subtitle {
          font-size: 0.85rem;
          color: var(--text-muted);
          margin: 0;
        }

        .modal-close {
          background: none;
          border: none;
          color: var(--text-muted);
          font-size: 1.5rem;
          cursor: pointer;
          padding: 0;
          width: 32px;
          height: 32px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 8px;
          transition: all 0.2s;
        }

        .modal-close:hover {
          background: rgba(255, 255, 255, 0.1);
          color: var(--text-main);
        }

        .recruiter-info-box {
          padding: 16px 24px;
          background: rgba(56, 189, 248, 0.05);
          border-left: 3px solid var(--accent-primary);
          margin: 0;
        }

        .recruiter-name {
          font-weight: 600;
          color: var(--text-main);
          margin-bottom: 8px;
        }

        .recruiter-link {
          color: var(--accent-primary);
          text-decoration: none;
          font-size: 0.9rem;
          transition: color 0.2s;
        }

        .recruiter-link:hover {
          color: #38BDF8;
          text-decoration: underline;
        }

        .outreach-tabs {
          display: flex;
          gap: 0;
          padding: 0 24px;
          border-bottom: 1px solid var(--border-color);
          margin-top: 0;
        }

        .tab-button {
          background: none;
          border: none;
          color: var(--text-muted);
          padding: 16px 20px;
          cursor: pointer;
          font-weight: 500;
          font-size: 0.9rem;
          border-bottom: 2px solid transparent;
          transition: all 0.2s;
          margin-bottom: -1px;
        }

        .tab-button:hover {
          color: var(--text-main);
        }

        .tab-button.active {
          color: var(--accent-primary);
          border-bottom-color: var(--accent-primary);
        }

        .outreach-content {
          padding: 24px;
        }

        .message-section {
          margin-bottom: 24px;
        }

        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 12px;
        }

        .section-title {
          font-weight: 600;
          color: var(--text-main);
          font-size: 0.95rem;
        }

        .edit-button {
          background: none;
          border: none;
          color: var(--accent-primary);
          cursor: pointer;
          font-size: 0.85rem;
          padding: 4px 8px;
          border-radius: 6px;
          transition: all 0.2s;
        }

        .edit-button:hover {
          background: rgba(56, 189, 248, 0.1);
        }

        .message-text {
          background: rgba(255, 255, 255, 0.02);
          border: 1px solid var(--border-color);
          border-radius: 10px;
          padding: 16px;
          color: var(--text-main);
          line-height: 1.6;
          font-size: 0.9rem;
        }

        .edit-form {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .edit-input,
        .edit-textarea {
          background: var(--input-bg);
          border: 1px solid var(--border-color);
          border-radius: 10px;
          padding: 12px;
          color: var(--text-main);
          font-family: var(--font-sans);
          font-size: 0.9rem;
        }

        .edit-input:focus,
        .edit-textarea:focus {
          outline: none;
          border-color: var(--accent-primary);
          box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
        }

        .edit-textarea {
          resize: vertical;
          min-height: 120px;
        }

        .edit-buttons {
          display: flex;
          gap: 10px;
        }

        .btn-small {
          padding: 8px 16px;
          font-size: 0.85rem;
        }

        .action-buttons {
          display: flex;
          gap: 12px;
          margin-top: 20px;
        }

        .action-buttons .btn {
          flex: 1;
        }

        .linkedin-note {
          font-size: 0.85rem;
          color: var(--text-muted);
          margin-top: 16px;
          padding: 12px;
          background: rgba(56, 189, 248, 0.05);
          border-radius: 8px;
          border-left: 3px solid var(--accent-primary);
        }

        .message-sections-preview {
          padding: 24px;
          border-top: 1px solid var(--border-color);
          background: rgba(255, 255, 255, 0.01);
        }

        .sections-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 16px;
          margin-top: 12px;
        }

        .section-card {
          background: rgba(255, 255, 255, 0.02);
          border: 1px solid var(--border-color);
          border-radius: 10px;
          padding: 16px;
        }

        .section-card h4 {
          margin: 0 0 8px 0;
          font-size: 0.9rem;
          color: var(--accent-primary);
          font-weight: 600;
        }

        .section-card p,
        .section-card ul {
          margin: 0;
          font-size: 0.85rem;
          color: var(--text-muted);
          line-height: 1.5;
        }

        .section-card ul {
          padding-left: 20px;
        }

        .section-card li {
          margin-bottom: 6px;
        }

        @media (max-width: 640px) {
          .modal-content {
            max-height: 95vh;
            border-radius: 16px;
          }

          .modal-header {
            flex-direction: column;
            gap: 12px;
          }

          .sections-grid {
            grid-template-columns: 1fr;
          }

          .action-buttons {
            flex-direction: column;
          }
        }
      `})]}),document.body)};export{c as default};