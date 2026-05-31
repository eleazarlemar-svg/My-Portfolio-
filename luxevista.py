import tkinter as tk
from tkinter import ttk, messagebox
import datetime

BG="#F0EDD8"; GOLD="#A9882E"; DARK="#1A1A1A"; WHITE="#FFFFFF"
CYAN="#00BFEA"; GREEN="#27AE60"; RED="#E74C3C"; MUTED="#7F8C8D"; CARD="#F5EDD0"

all_users={}; all_bookings=[]; all_ratings=[]; current_user={}
ROOMS=["Twin Room","Queen Room","Triple Room","Triple Room XL","Deluxe Ocean View","Family Room"]
PRICES={"Twin Room":4500,"Queen Room":6000,"Triple Room":7500,
        "Triple Room XL":8500,"Deluxe Ocean View":10000,"Family Room":14000}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LuxeVista Hotel"); self.geometry("420x780")
        self.resizable(False,False); self.configure(bg=BG)
        self.frame=None; self.show_page("Login")

    def show_page(self, name, **kw):
        if self.frame: self.frame.destroy()
        pages={"Login":LoginPage,"Register":RegisterPage,"Home":HomePage,"Book":BookPage,
               "Reservations":ReservationsPage,"Rooms":RoomsPage,"Spa":SpaPage,
               "Ratings":RatingsPage,"Profile":ProfilePage,"Checkin":CheckinPage,"Checkout":CheckoutPage}
        self.frame=pages[name](self,self,**kw); self.frame.pack(fill="both",expand=True)


def make_header(parent, app, title="LuxeVista", back=None):
    bar=tk.Frame(parent,bg=DARK,height=58); bar.pack(fill="x"); bar.pack_propagate(False)
    tk.Label(bar,text="LuxeVista",font=("Georgia",13,"bold"),bg=DARK,fg=GOLD).pack(side="left",padx=14,pady=14)
    tk.Label(bar,text=title,font=("Helvetica",10),bg=DARK,fg=WHITE).pack(side="right",padx=10)
    if back:
        tk.Button(bar,text="< Back",font=("Helvetica",9),bg=DARK,fg=GOLD,bd=0,cursor="hand2",
                  activebackground=DARK,command=lambda:app.show_page(back)).pack(side="right",padx=8)

def make_navbar(parent, app):
    bar=tk.Frame(parent,bg=DARK,height=56); bar.pack(side="bottom",fill="x"); bar.pack_propagate(False)
    for lbl,pg in [("Home","Home"),("Reservations","Reservations"),("Ratings","Ratings"),("Profile","Profile")]:
        tk.Button(bar,text=lbl,font=("Helvetica",9,"bold"),bg=DARK,fg=GOLD,bd=0,cursor="hand2",
                  activebackground="#2A2A2A",command=lambda p=pg:app.show_page(p)).pack(side="left",expand=True,fill="y")

def big_btn(parent, text, cmd, color=GOLD):
    tk.Button(parent,text=text,font=("Helvetica",11,"bold"),bg=color,fg=WHITE,bd=0,
              pady=10,cursor="hand2",command=cmd).pack(pady=5,padx=20,fill="x")

def lbl_entry(parent, label, bg=BG, secret=False):
    tk.Label(parent,text=label,font=("Helvetica",10,"bold"),bg=bg,fg=DARK,anchor="w").pack(fill="x",padx=24,pady=(6,0))
    v=tk.StringVar()
    tk.Entry(parent,textvariable=v,font=("Helvetica",10),bg=WHITE,bd=0,
             highlightthickness=1,highlightbackground=GOLD,show="*" if secret else "").pack(fill="x",padx=24,ipady=8,pady=(2,4))
    return v

def scroll_inner(parent):
    c=tk.Canvas(parent,bg=BG,bd=0,highlightthickness=0)
    sb=ttk.Scrollbar(parent,orient="vertical",command=c.yview)
    inner=tk.Frame(c,bg=BG)
    inner.bind("<Configure>",lambda e:c.configure(scrollregion=c.bbox("all")))
    c.create_window((0,0),window=inner,anchor="nw",width=400)
    c.configure(yscrollcommand=sb.set)
    c.pack(side="left",fill="both",expand=True); sb.pack(side="right",fill="y")
    return inner


class LoginPage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent,bg=BG); self.app=app
        tk.Label(self,text="LuxeVista",font=("Georgia",28,"bold"),bg=BG,fg=GOLD).pack(pady=(50,2))
        tk.Label(self,text="LUXURY RESORTS & HOTELS",font=("Helvetica",9),bg=BG,fg=MUTED).pack()
        tk.Label(self,text="Welcome Back!",font=("Georgia",20,"bold"),bg=BG,fg=DARK).pack(pady=(20,2))
        tk.Label(self,text="Login to continue your booking",font=("Helvetica",10),bg=BG,fg=MUTED).pack(pady=(0,18))
        self.email=lbl_entry(self,"Email Address")
        self.passw=lbl_entry(self,"Password",secret=True)
        tk.Label(self,text="Forgot password?",font=("Helvetica",9),bg=BG,fg=CYAN,anchor="e").pack(fill="x",padx=24)
        tk.Frame(self,bg=BG,height=10).pack()
        big_btn(self,"Log In",self.do_login,CYAN)
        tk.Label(self,text="or",font=("Helvetica",9),bg=BG,fg=MUTED).pack(pady=4)
        tk.Button(self,text="Create Account",font=("Helvetica",11,"bold"),bg=WHITE,fg=GOLD,bd=1,
                  relief="solid",padx=8,pady=8,width=28,cursor="hand2",
                  command=lambda:app.show_page("Register")).pack()

    def do_login(self):
        em,pw=self.email.get().strip(),self.passw.get().strip()
        if not em or not pw: messagebox.showwarning("Empty","Please fill in all fields."); return
        if em in all_users and all_users[em]["password"]==pw:
            current_user.update(all_users[em]); current_user["email"]=em; self.app.show_page("Home")
        else: messagebox.showerror("Failed","Invalid email or password.")


class RegisterPage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent,bg=BG); self.app=app
        tk.Label(self,text="LuxeVista",font=("Georgia",22,"bold"),bg=BG,fg=GOLD).pack(pady=(30,2))
        tk.Label(self,text="Create Your Account",font=("Georgia",20,"bold"),bg=BG,fg=DARK).pack(pady=(10,2))
        tk.Label(self,text="Fill in the details below to get started",font=("Helvetica",10),bg=BG,fg=MUTED).pack(pady=(0,10))
        self.name=lbl_entry(self,"Full Name")
        self.email=lbl_entry(self,"Email Address")
        self.phone=lbl_entry(self,"Phone Number (+63)")
        self.passw=lbl_entry(self,"Password",secret=True)
        self.passw2=lbl_entry(self,"Confirm Password",secret=True)
        tk.Label(self,text="At least 8 characters with letters and numbers",font=("Helvetica",9),bg=BG,fg=MUTED).pack()
        tk.Frame(self,bg=BG,height=8).pack()
        big_btn(self,"Create Account",self.do_register,CYAN)
        tk.Button(self,text="Already have an account? Log in",font=("Helvetica",9),bg=BG,fg=GOLD,
                  bd=0,cursor="hand2",command=lambda:app.show_page("Login")).pack(pady=6)

    def do_register(self):
        n,em,ph=self.name.get().strip(),self.email.get().strip(),self.phone.get().strip()
        pw,pw2=self.passw.get(),self.passw2.get()
        if not all([n,em,ph,pw,pw2]): messagebox.showwarning("Missing","Please complete all fields."); return
        if pw!=pw2: messagebox.showerror("Mismatch","Passwords do not match."); return
        if len(pw)<8: messagebox.showerror("Short","Password must be at least 8 characters."); return
        if em in all_users: messagebox.showerror("Exists","Email already registered."); return
        all_users[em]={"name":n,"phone":ph,"password":pw}
        messagebox.showinfo("Success!","Account created! Please log in."); self.app.show_page("Login")


class HomePage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent,bg=BG); self.app=app
        make_header(self,app)
        hero=tk.Frame(self,bg=DARK,height=160); hero.pack(fill="x"); hero.pack_propagate(False)
        tk.Label(hero,text="🏨",font=("Helvetica",70),bg=DARK).pack(expand=True)
        tk.Label(self,text="A new window into luxury",font=("Georgia",15,"bold"),bg=BG,fg=DARK).pack(pady=(12,0))
        tk.Label(self,text="Your Perfect Stay Starts Here",font=("Helvetica",10),bg=BG,fg=GOLD).pack()
        pill=tk.Frame(self,bg=WHITE,pady=10,padx=8); pill.pack(fill="x",padx=18,pady=10)
        pill.columnconfigure((0,1,2),weight=1)
        for i,(lbl,pg) in enumerate([("Check-in","Checkin"),("Check-out","Checkout"),("Guest","Reservations")]):
            tk.Button(pill,text=lbl,font=("Helvetica",10,"bold"),bg="#F0F0F0",fg=DARK,bd=0,
                      relief="flat",padx=6,pady=10,cursor="hand2",
                      command=lambda p=pg:app.show_page(p)).grid(row=0,column=i,padx=4,sticky="ew")
        big_btn(self,"  BOOK NOW",lambda:app.show_page("Book"))
        cats=tk.Frame(self,bg=BG); cats.pack(fill="x",padx=18,pady=4)
        cats.columnconfigure((0,1),weight=1)
        for col,(lbl,pg) in enumerate([("Rooms","Rooms"),("Spa","Spa")]):
            tk.Button(cats,text=lbl,font=("Helvetica",13,"bold"),bg=CARD,fg=DARK,bd=0,
                      relief="flat",padx=10,pady=28,cursor="hand2",
                      command=lambda p=pg:app.show_page(p)).grid(row=0,column=col,padx=6,sticky="nsew")
        make_navbar(self,app)


class BookPage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent,bg=BG); self.app=app
        make_header(self,app,"Book Now",back="Home")
        tk.Label(self,text="BOOK NOW",font=("Georgia",20,"bold"),bg=BG,fg=GOLD).pack(pady=(12,2))
        tk.Label(self,text="Your Perfect Stay Starts Here",font=("Helvetica",9),bg=BG,fg=MUTED).pack()
        card=tk.Frame(self,bg=WHITE,padx=16,pady=14); card.pack(fill="x",padx=18,pady=10)

        def ce(lbl, val=""):  # card entry helper
            tk.Label(card,text=lbl,font=("Helvetica",9,"bold"),bg=WHITE,fg=DARK,anchor="w").pack(fill="x")
            v=tk.StringVar(value=val)
            tk.Entry(card,textvariable=v,font=("Helvetica",9),bg="#F9F9F9",bd=0,
                     highlightthickness=1,highlightbackground=GOLD).pack(fill="x",ipady=6,pady=(2,8))
            return v

        self.gname=ce("Full Name",current_user.get("name",""))
        self.gemail=ce("Email",current_user.get("email",""))
        today=datetime.date.today().strftime("%Y-%m-%d")
        tomorrow=(datetime.date.today()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        row=tk.Frame(card,bg=WHITE); row.pack(fill="x"); row.columnconfigure((0,1),weight=1)
        for col,(lbl,val,attr) in enumerate([("Check-in (YYYY-MM-DD)",today,"cin"),("Check-out (YYYY-MM-DD)",tomorrow,"cout")]):
            side=tk.Frame(row,bg=WHITE); side.grid(row=0,column=col,padx=4,sticky="ew")
            tk.Label(side,text=lbl,font=("Helvetica",9),bg=WHITE,fg=DARK,anchor="w").pack(fill="x")
            v=tk.StringVar(value=val); setattr(self,attr,v)
            tk.Entry(side,textvariable=v,font=("Helvetica",9),bg="#F9F9F9",bd=0,
                     highlightthickness=1,highlightbackground=GOLD).pack(fill="x",ipady=5,pady=(2,8))
        tk.Label(card,text="Number of Guests",font=("Helvetica",9,"bold"),bg=WHITE,fg=DARK,anchor="w").pack(fill="x")
        self.guests=ttk.Combobox(card,font=("Helvetica",9),state="readonly",
                                  values=["1 Adult","2 Adults","3 Adults","2 Adults + 1 Kid","Family (4+)"])
        self.guests.set("Select guests"); self.guests.pack(fill="x",ipady=3,pady=(2,8))
        tk.Label(card,text="Choose Your Room",font=("Helvetica",9,"bold"),bg=WHITE,fg=DARK,anchor="w").pack(fill="x")
        self.room=ttk.Combobox(card,font=("Helvetica",9),state="readonly",values=ROOMS)
        self.room.set("Select room type"); self.room.pack(fill="x",ipady=3,pady=(2,4))
        big_btn(self,"BOOK NOW",self.confirm_booking); make_navbar(self,app)

    def confirm_booking(self):
        name,email=self.gname.get().strip(),self.gemail.get().strip()
        cin,cout=self.cin.get().strip(),self.cout.get().strip()
        guests,room=self.guests.get(),self.room.get()
        if not all([name,email,cin,cout]) or "Select" in guests or "Select" in room:
            messagebox.showwarning("Incomplete","Please fill in all fields."); return
        try:
            d1,d2=datetime.date.fromisoformat(cin),datetime.date.fromisoformat(cout)
            nights=(d2-d1).days
            if nights<=0: raise ValueError
        except ValueError: messagebox.showerror("Date Error","Check-out must be after Check-in."); return
        rate=PRICES.get(room,6000); sub=rate*nights; tax=int(sub*0.20); total=sub+tax
        b={"id":f"LV{1000+len(all_bookings)+1}","name":name,"email":email,"cin":cin,"cout":cout,
           "nights":nights,"guests":guests,"room":room,"rate":rate,"sub":sub,"tax":tax,"total":total,
           "status":"Confirmed","booked_on":str(datetime.date.today())}
        all_bookings.append(b)
        messagebox.showinfo("Booking Confirmed!",
            f"Booking ID  : {b['id']}\nRoom        : {room}\nCheck-in    : {cin}\n"
            f"Check-out   : {cout}\nNights      : {nights}\nGuests      : {guests}\n"
            f"Room Rate   : P{sub:,}\nTax & Fees  : P{tax:,}\nTOTAL PAID  : P{total:,}")
        self.app.show_page("Home")


class ReservationsPage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent,bg=BG)
        make_header(self,app,"Reservations",back="Home")
        tk.Label(self,text="My Reservations",font=("Georgia",14,"bold"),bg=BG,fg=DARK).pack(pady=12)
        inner=scroll_inner(self)
        my=[b for b in all_bookings if b.get("email")==current_user.get("email","")]
        if not my:
            tk.Label(inner,text="No reservations yet.\nBook a room to get started!",
                     font=("Helvetica",10),bg=BG,fg=MUTED,justify="center").pack(pady=50)
        else:
            for b in reversed(my):
                card=tk.Frame(inner,bg=WHITE,pady=12,padx=16); card.pack(fill="x",padx=12,pady=6)
                tk.Label(card,text=f"  {b['room']}",font=("Helvetica",12,"bold"),bg=WHITE,fg=DARK).pack(anchor="w")
                tk.Label(card,text=f"  {b['cin']} to {b['cout']} ({b['nights']} nights)",
                         font=("Helvetica",9),bg=WHITE,fg=MUTED).pack(anchor="w")
                tk.Label(card,text=f"  Guests: {b['guests']}   ID: {b['id']}",
                         font=("Helvetica",9),bg=WHITE,fg=MUTED).pack(anchor="w")
                tk.Label(card,text=f"  {b['status']}   P{b['total']:,}",font=("Helvetica",10,"bold"),
                         bg=WHITE,fg=GREEN if b["status"]=="Confirmed" else RED).pack(anchor="w",pady=(4,0))
        make_navbar(self,app)


class RoomsPage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent,bg=BG)
        make_header(self,app,"Rooms",back="Home")
        tk.Label(self,text="Room Rates",font=("Georgia",17,"bold"),bg=BG,fg=GOLD).pack(pady=(10,2))
        tk.Label(self,text="Stay in Luxury, Wake up to the View",font=("Helvetica",9),bg=BG,fg=MUTED).pack()
        inner=scroll_inner(self)
        for name,beds,occ,price in [
            ("Twin Room","2 Single Beds","Max 2 Adults",4500),
            ("Queen Room","1 Queen Bed + Balcony","Max 2 Adults + 1 Kid",6000),
            ("Triple Room","1 Queen + 1 Single","Max 3 Adults",7500),
            ("Triple Room XL","3 Single + 1 Queen","Max 3 Adults + 1 Kid",8500),
            ("Deluxe Ocean View","1 King Bed, Ocean View","Max 2 Adults",10000),
            ("Family Room","2 Queen + 1 Single","Max 6 Adults + 2 Kids",14000)]:
            card=tk.Frame(inner,bg=WHITE,pady=10,padx=14); card.pack(fill="x",padx=10,pady=5)
            top=tk.Frame(card,bg=WHITE); top.pack(fill="x")
            tk.Label(top,text=f"  {name}",font=("Helvetica",12,"bold"),bg=WHITE,fg=DARK).pack(side="left")
            tk.Label(top,text=f"P{price:,}/night",font=("Helvetica",11,"bold"),bg=WHITE,fg=GOLD).pack(side="right")
            tk.Label(card,text=f"   {beds}  |  {occ}",font=("Helvetica",9),bg=WHITE,fg=MUTED).pack(anchor="w")
            tk.Label(card,text="   Free WiFi  |  Air-Con  |  Mini Fridge  |  Toiletries",
                     font=("Helvetica",8),bg=WHITE,fg=MUTED).pack(anchor="w")
            tk.Button(card,text="Book This Room",font=("Helvetica",9),bg=GOLD,fg=WHITE,bd=0,
                      cursor="hand2",padx=8,pady=4,command=lambda:app.show_page("Book")).pack(anchor="e",pady=(4,0))
        make_navbar(self,app)


class SpaPage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent,bg=BG)
        make_header(self,app,"Spa",back="Home")
        tk.Label(self,text="Spa & Wellness",font=("Georgia",17,"bold"),bg=BG,fg=DARK).pack(pady=(12,2))
        tk.Label(self,text="Relax. Rejuvenate. Restore.",font=("Helvetica",9),bg=BG,fg=MUTED).pack()
        for name,desc,price in [
            ("Wellness Massage","Relieve stress and improve circulation.","P1,500/session"),
            ("Signature Facial","Deep cleanse and skin revitalization.","P1,800/session"),
            ("Aroma Therapy Massage","Essential oils for mind and body balance.","P2,000/session"),
            ("Hot Stone Therapy","Relaxes muscles and enhances relaxation.","P2,300/session"),
            ("Sauna and Steam","Detoxify and improve blood circulation.","P1,000/session")]:
            card=tk.Frame(self,bg=WHITE,pady=12,padx=16); card.pack(fill="x",padx=18,pady=5)
            top=tk.Frame(card,bg=WHITE); top.pack(fill="x")
            tk.Label(top,text=name,font=("Helvetica",11,"bold"),bg=WHITE,fg=DARK).pack(side="left")
            tk.Label(top,text=price,font=("Helvetica",10,"bold"),bg=WHITE,fg=GOLD).pack(side="right")
            tk.Label(card,text=desc,font=("Helvetica",9),bg=WHITE,fg=MUTED,anchor="w").pack(fill="x")
        make_navbar(self,app)


def build_inout_page(frame, app, is_checkin):
    title="Check-in" if is_checkin else "Check-out"
    make_header(frame,app,title,back="Home")
    tk.Label(frame,text=f"{title} Details",font=("Georgia",14,"bold"),bg=BG,fg=DARK).pack(pady=14)
    my=[b for b in all_bookings if b.get("email")==current_user.get("email","")]
    if not my:
        tk.Label(frame,text="No active bookings found.\nPlease make a reservation first.",
                 font=("Helvetica",10),bg=BG,fg=MUTED,justify="center").pack(pady=30)
        if is_checkin: big_btn(frame,"Book Now",lambda:app.show_page("Book"))
    else:
        b=my[-1]
        info=tk.Frame(frame,bg=WHITE,padx=20,pady=16); info.pack(fill="x",padx=20,pady=8)
        tk.Label(info,text=f"{title} Date & Time",font=("Helvetica",11,"bold"),bg=WHITE,fg=GOLD).pack(anchor="w")
        date_str=f"{b['cin']}  at  2:00 PM" if is_checkin else f"{b['cout']}  at  12:00 PM"
        tk.Label(info,text=date_str,font=("Georgia",13,"bold"),bg=WHITE,fg=DARK).pack(anchor="w",pady=(2,10))
        steps=[("Arrival & Welcome","Our staff will greet you."),
               ("ID Verification","Please present a valid government ID."),
               ("Room Key","Receive your room key and WiFi access.")] if is_checkin else [
              ("Express Check-out","Quick and seamless process."),
              ("Bill Settlement","We will review charges and process payment."),
              ("Thank You!","Thank you for staying. Hope to see you again!")]
        for t,d in steps:
            tk.Label(info,text=t,font=("Helvetica",10,"bold"),bg=WHITE,fg=DARK).pack(anchor="w")
            tk.Label(info,text=d,font=("Helvetica",9),bg=WHITE,fg=MUTED).pack(anchor="w",pady=(0,6))
        note=tk.Frame(frame,bg=CARD,padx=14,pady=10); note.pack(fill="x",padx=20,pady=6)
        q="Need early check-in?" if is_checkin else "Need late check-out?"
        tk.Label(note,text=q,font=("Helvetica",10,"bold"),bg=CARD,fg=DARK).pack(anchor="w")
        tk.Label(note,text="Contact our front desk for availability.",font=("Helvetica",9),bg=CARD,fg=MUTED).pack(anchor="w")
    make_navbar(frame,app)

class CheckinPage(tk.Frame):
    def __init__(self,parent,app,**kw):
        super().__init__(parent,bg=BG); build_inout_page(self,app,is_checkin=True)

class CheckoutPage(tk.Frame):
    def __init__(self,parent,app,**kw):
        super().__init__(parent,bg=BG); build_inout_page(self,app,is_checkin=False)


class RatingsPage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent,bg=BG); self.app=app; self.star_count=0; self.star_btns=[]
        make_header(self,app,"Ratings",back="Home")
        tk.Label(self,text="Rate Your Stay",font=("Georgia",14,"bold"),bg=BG,fg=DARK).pack(pady=(14,2))
        tk.Label(self,text="Your feedback helps us improve!",font=("Helvetica",9),bg=BG,fg=MUTED).pack()
        sf=tk.Frame(self,bg=BG); sf.pack(pady=12)
        for i in range(1,6):
            btn=tk.Button(sf,text="*",font=("Helvetica",28),bg=BG,fg=GOLD,bd=0,
                          cursor="hand2",activebackground=BG,command=lambda s=i:self.pick_star(s))
            btn.pack(side="left",padx=2); self.star_btns.append(btn)
        tk.Label(self,text="Write a Review",font=("Helvetica",10,"bold"),bg=BG,fg=DARK,anchor="w").pack(fill="x",padx=24)
        self.review_box=tk.Text(self,font=("Helvetica",10),height=4,bd=0,
                                highlightthickness=1,highlightbackground=GOLD,wrap="word")
        self.review_box.pack(fill="x",padx=24,pady=(4,8))
        big_btn(self,"Submit Rating",self.submit_rating)
        tk.Label(self,text="Guest Reviews",font=("Helvetica",10,"bold"),bg=BG,fg=GOLD).pack(pady=(10,4))
        self.reviews_area=tk.Frame(self,bg=BG); self.reviews_area.pack(fill="both",expand=True,padx=18)
        self.load_reviews(); make_navbar(self,app)

    def pick_star(self, count):
        self.star_count=count
        for i,btn in enumerate(self.star_btns):
            btn.config(text="*" if i<count else "-",fg=GOLD if i<count else MUTED)

    def submit_rating(self):
        if self.star_count==0: messagebox.showwarning("No Rating","Please select a star rating first."); return
        rev=self.review_box.get("1.0","end").strip()
        all_ratings.append({"user":current_user.get("name","Guest"),"stars":self.star_count,
                             "review":rev if rev else "No comment.","date":str(datetime.date.today())})
        messagebox.showinfo("Thank you!",f"You rated us {self.star_count} star(s). We appreciate it!")
        self.pick_star(0); self.review_box.delete("1.0","end"); self.load_reviews()

    def load_reviews(self):
        for w in self.reviews_area.winfo_children(): w.destroy()
        if not all_ratings:
            tk.Label(self.reviews_area,text="No reviews yet. Be the first!",font=("Helvetica",9),bg=BG,fg=MUTED).pack(pady=10); return
        for r in reversed(all_ratings[-5:]):
            card=tk.Frame(self.reviews_area,bg=WHITE,pady=8,padx=12); card.pack(fill="x",pady=4)
            top=tk.Frame(card,bg=WHITE); top.pack(fill="x")
            tk.Label(top,text=r["user"],font=("Helvetica",10,"bold"),bg=WHITE,fg=DARK).pack(side="left")
            tk.Label(top,text=("*"*r["stars"])+("-"*(5-r["stars"])),
                     font=("Helvetica",13,"bold"),bg=WHITE,fg=GOLD).pack(side="right")
            tk.Label(card,text=r["review"],font=("Helvetica",9),bg=WHITE,fg=MUTED,
                     wraplength=310,justify="left",anchor="w").pack(fill="x")
            tk.Label(card,text=r["date"],font=("Helvetica",7),bg=WHITE,fg="#BBBBBB").pack(anchor="e")


class ProfilePage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent,bg=BG); self.app=app
        make_header(self,app,"Profile",back="Home")
        av=tk.Frame(self,bg=DARK,width=72,height=72); av.pack(pady=(20,8)); av.pack_propagate(False)
        tk.Label(av,text="U",font=("Georgia",30,"bold"),bg=DARK,fg=GOLD).pack(expand=True)
        name=current_user.get("name","Guest"); email=current_user.get("email","--"); phone=current_user.get("phone","--")
        tk.Label(self,text=name,font=("Georgia",15,"bold"),bg=BG,fg=DARK).pack()
        tk.Label(self,text=email,font=("Helvetica",9),bg=BG,fg=MUTED).pack(pady=(0,12))
        card=tk.Frame(self,bg=WHITE,pady=16,padx=20); card.pack(fill="x",padx=20)
        tk.Label(card,text="Personal Details",font=("Helvetica",12,"bold"),bg=WHITE,fg=GOLD).pack(anchor="w")
        tk.Frame(card,bg=GOLD,height=1).pack(fill="x",pady=6)
        for label,val in [("Full Name",name),("Email",email),("Phone",phone)]:
            row=tk.Frame(card,bg=WHITE); row.pack(fill="x",pady=4)
            tk.Label(row,text=label,font=("Helvetica",9),bg=WHITE,fg=MUTED,width=14,anchor="w").pack(side="left")
            tk.Label(row,text=val,font=("Helvetica",10,"bold"),bg=WHITE,fg=DARK).pack(side="left")
        tk.Frame(self,bg=BG,height=16).pack()
        tk.Button(self,text="Log Out",font=("Helvetica",11,"bold"),bg=RED,fg=WHITE,bd=0,
                  padx=20,pady=10,width=28,cursor="hand2",activebackground="#C0392B",
                  command=self.logout).pack()
        make_navbar(self,app)

    def logout(self):
        if messagebox.askyesno("Log Out","Are you sure you want to log out?"):
            current_user.clear(); self.app.show_page("Login")


if __name__=="__main__":
    all_users["demo@luxevista.com"]={"name":"Juan Dela Cruz","phone":"+63 962 553 1020","password":"demo1234"}
    App().mainloop()
