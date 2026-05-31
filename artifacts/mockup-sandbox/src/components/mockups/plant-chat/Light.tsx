import React, { useState, useEffect, useRef } from "react";
import { Check, X, Send, MoreVertical, Search, Paperclip, Smile, FastForward } from "lucide-react";

// Types
type PlantSpecies = "Jiboia" | "Samambaia" | "Cacto" | "Orquídea";

interface Plant {
  id: string;
  name: string;
  species: PlantSpecies;
  emoji: string;
  color: string;
}

type MessageStatus = "pending" | "accepted" | "rejected";

interface Message {
  id: string;
  plantId: string;
  text: string;
  time: string;
  status: MessageStatus;
  isOwner?: boolean;
}

// Mock Data
const PLANTS: Plant[] = [
  { id: "p1", name: "Fernanda", species: "Jiboia", emoji: "🌿", color: "bg-green-100 text-green-700" },
  { id: "p2", name: "Samuca", species: "Samambaia", emoji: "🪴", color: "bg-emerald-100 text-emerald-700" },
  { id: "p3", name: "Espeto", species: "Cacto", emoji: "🌵", color: "bg-lime-100 text-lime-700" },
  { id: "p4", name: "Madame", species: "Orquídea", emoji: "🌸", color: "bg-fuchsia-100 text-fuchsia-700" },
];

const INITIAL_MESSAGES: Message[] = [
  { id: "m1", plantId: "p1", text: "Tô morrendo de sede, me rega logo! 🥵", time: "09:00", status: "pending" },
  { id: "m2", plantId: "p2", text: "Você me colocou num lugar com muito sol. Tô queimando! ☀️🔥", time: "10:30", status: "rejected" },
  { id: "m3", plantId: "p3", text: "Acho que vi um bicho na minha terra. Faz alguma coisa! 🐛", time: "11:15", status: "accepted" },
  { id: "m4", plantId: "p1", text: "Coloque a planta Fernanda na geladeira. Tá muito calor aqui fora.", time: "12:00", status: "pending" },
  { id: "m5", plantId: "p4", text: "Exijo adubo novo. Esse já perdeu o gosto. 💅", time: "14:20", status: "pending" },
];

const CRAZY_REQUESTS = [
  "Me canta uma música? Tô me sentindo sozinha.",
  "Coloca um cubo de gelo na minha terra, por favor.",
  "Tira o Espeto de perto de mim, ele me furou ontem!",
  "Acho que tô virando uma árvore. Preciso de um vaso maior.",
  "Me leva pra passear no parque? 🥺",
  "Põe aquela playlist de rock pauleira pra eu crescer mais forte.",
  "Mais água! Mais água! MAIS ÁGUA! 🌊",
  "Seca minhas folhas com o secador? Tomei banho e tô com frio.",
  "Me vira pra janela, quero ver o movimento da rua.",
  "Limpa minhas folhas, tô cheia de poeira. Que falta de modos.",
];

const generateTime = () => {
  const now = new Date();
  return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
};

export function Light() {
  const [messages, setMessages] = useState<Message[]>(INITIAL_MESSAGES);
  const [activePlantId, setActivePlantId] = useState<string>(PLANTS[0].id);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const activePlant = PLANTS.find(p => p.id === activePlantId)!;
  const activeMessages = messages.filter(m => m.plantId === activePlantId);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeMessages.length]);

  const handleAction = (messageId: string, status: MessageStatus) => {
    setMessages(prev => prev.map(m => m.id === messageId ? { ...m, status } : m));
  };

  const handleNovoTurno = () => {
    const newMessages: Message[] = PLANTS.map(plant => ({
      id: Math.random().toString(36).substring(7),
      plantId: plant.id,
      text: CRAZY_REQUESTS[Math.floor(Math.random() * CRAZY_REQUESTS.length)],
      time: generateTime(),
      status: "pending"
    }));

    setMessages(prev => [...prev, ...newMessages]);
  };

  const getLastMessageText = (plantId: string) => {
    const plantMessages = messages.filter(m => m.plantId === plantId);
    if (plantMessages.length === 0) return "";
    return plantMessages[plantMessages.length - 1].text;
  };

  const getUnreadCount = (plantId: string) => {
    return messages.filter(m => m.plantId === plantId && m.status === "pending").length;
  };

  return (
    <div className="flex h-[100dvh] w-full bg-slate-100 overflow-hidden font-sans text-slate-800">
      
      {/* SIDEBAR */}
      <div className="w-[30%] min-w-[320px] max-w-[400px] flex flex-col bg-white border-r border-slate-200 z-10">
        
        {/* Sidebar Header */}
        <div className="h-16 bg-slate-50 flex items-center justify-between px-4 py-2 border-b border-slate-200">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-slate-200 flex items-center justify-center text-xl overflow-hidden">
              🧑‍🌾
            </div>
            <span className="font-semibold text-slate-700">Meu Jardim</span>
          </div>
          <div className="flex text-slate-500 gap-4">
            <MoreVertical className="w-5 h-5 cursor-pointer hover:text-slate-700 transition-colors" />
          </div>
        </div>

        {/* Search */}
        <div className="p-3 bg-white border-b border-slate-100">
          <div className="bg-slate-100 rounded-lg flex items-center px-3 py-1.5 border border-slate-200 focus-within:bg-white focus-within:border-green-400 transition-colors shadow-sm">
            <Search className="w-4 h-4 text-slate-400 mr-2" />
            <input 
              type="text" 
              placeholder="Pesquisar plantinha..." 
              className="bg-transparent border-none outline-none text-sm w-full text-slate-700 placeholder:text-slate-400"
            />
          </div>
        </div>

        {/* Contact List */}
        <div className="flex-1 overflow-y-auto">
          {PLANTS.map(plant => {
            const unreadCount = getUnreadCount(plant.id);
            const isActive = activePlantId === plant.id;
            
            return (
              <div 
                key={plant.id}
                onClick={() => setActivePlantId(plant.id)}
                className={`flex items-center px-4 py-3 cursor-pointer border-b border-slate-100 transition-colors ${
                  isActive ? 'bg-green-50' : 'hover:bg-slate-50'
                }`}
              >
                <div className={`w-12 h-12 rounded-full flex flex-shrink-0 items-center justify-center text-2xl ${plant.color} shadow-sm border border-black/5`}>
                  {plant.emoji}
                </div>
                <div className="ml-4 flex-1 min-w-0">
                  <div className="flex justify-between items-baseline mb-0.5">
                    <span className="font-medium text-slate-800">{plant.name}</span>
                    <span className="text-xs text-green-600 font-medium">
                      {messages.filter(m => m.plantId === plant.id).pop()?.time}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className={`text-sm truncate pr-2 ${isActive ? 'text-slate-700' : 'text-slate-500'}`}>
                      {getLastMessageText(plant.id)}
                    </span>
                    {unreadCount > 0 && (
                      <span className="bg-[#25D366] text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full min-w-[20px] text-center">
                        {unreadCount}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* MAIN CHAT AREA */}
      <div className="flex-1 flex flex-col relative bg-[#EFEAE2]">
        {/* Chat Background Watermark (CSS pattern) */}
        <div 
          className="absolute inset-0 z-0 opacity-[0.06] pointer-events-none"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cpath d='M30 60c-16.569 0-30-13.431-30-30C0 13.431 13.431 0 30 0c16.569 0 30 13.431 30 30 0 16.569-13.431 30-30 30zm0-2c15.464 0 28-12.536 28-28S45.464 2 30 2 2 14.536 2 30s12.536 28 28 28z' fill='%23000000' fill-opacity='1'/%3E%3Cpath d='M30 45a15 15 0 1 0 0-30 15 15 0 0 0 0 30zm0-2a13 13 0 1 1 0-26 13 13 0 0 1 0 26z' fill='%23000000' fill-opacity='1'/%3E%3Cpath d='M30 35a5 5 0 1 0 0-10 5 5 0 0 0 0 10zm0-2a3 3 0 1 1 0-6 3 3 0 0 1 0 6z' fill='%23000000' fill-opacity='1'/%3E%3C/g%3E%3C/svg%3E")`,
            backgroundSize: '120px 120px'
          }}
        />

        {/* Chat Header */}
        <div className="h-16 bg-slate-50 flex items-center justify-between px-4 py-2 border-b border-slate-200 z-10 shadow-sm">
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center text-xl ${activePlant.color}`}>
              {activePlant.emoji}
            </div>
            <div>
              <div className="font-semibold text-slate-800">{activePlant.name}</div>
              <div className="text-xs text-slate-500">{activePlant.species} • online</div>
            </div>
          </div>
          <div className="flex text-slate-500 gap-5 px-2">
            <Search className="w-5 h-5 cursor-pointer hover:text-slate-700 transition-colors" />
            <MoreVertical className="w-5 h-5 cursor-pointer hover:text-slate-700 transition-colors" />
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 z-10 scroll-smooth">
          <div className="flex flex-col gap-4 max-w-3xl mx-auto pb-4">
            
            <div className="text-center my-2">
              <span className="bg-white/80 text-slate-500 text-xs px-3 py-1 rounded-md shadow-sm border border-slate-100 uppercase tracking-wider font-medium">
                Hoje
              </span>
            </div>

            {activeMessages.map((msg, index) => {
              const showTail = index === 0 || activeMessages[index - 1].isOwner !== msg.isOwner;
              
              if (msg.isOwner) {
                return (
                  <div key={msg.id} className="flex justify-end mb-1">
                    <div className="bg-[#d9fdd3] text-slate-800 p-2.5 rounded-lg max-w-[70%] shadow-sm relative rounded-tr-none">
                      {showTail && (
                        <div className="absolute top-0 right-[-8px] w-0 h-0 border-l-[8px] border-l-[#d9fdd3] border-t-[0px] border-t-transparent border-b-[10px] border-b-transparent"></div>
                      )}
                      <p className="text-[15px] leading-snug">{msg.text}</p>
                      <div className="text-[11px] text-slate-500 text-right mt-1 ml-4 flex justify-end items-center gap-1">
                        {msg.time}
                        <Check className="w-3 h-3 text-blue-500 inline" strokeWidth={3} />
                      </div>
                    </div>
                  </div>
                );
              }

              // Plant Message
              return (
                <div key={msg.id} className="flex justify-start mb-1 group">
                  <div className={`
                    p-3 rounded-lg max-w-[80%] shadow-sm relative rounded-tl-none transition-all duration-300
                    ${msg.status === 'accepted' ? 'bg-[#e8fbe8] border border-green-200' : 
                      msg.status === 'rejected' ? 'bg-slate-50 border border-slate-200 opacity-75' : 
                      'bg-white border border-transparent'}
                  `}>
                    {showTail && (
                      <div className={`
                        absolute top-0 left-[-8px] w-0 h-0 border-r-[8px] border-t-[0px] border-t-transparent border-b-[10px] border-b-transparent
                        ${msg.status === 'accepted' ? 'border-r-[#e8fbe8]' : 
                          msg.status === 'rejected' ? 'border-r-slate-50' : 
                          'border-r-white'}
                      `}></div>
                    )}
                    
                    <div className="font-semibold text-[13px] text-green-600 mb-1 leading-tight">
                      {activePlant.name}
                    </div>
                    
                    <div className="flex flex-col gap-2">
                      <p className={`text-[15px] leading-snug ${msg.status === 'rejected' ? 'text-slate-400 line-through' : 'text-slate-800'}`}>
                        {msg.text}
                      </p>
                      
                      {msg.status === "pending" && (
                        <div className="flex gap-2 mt-2 pt-2 border-t border-slate-100">
                          <button 
                            onClick={() => handleAction(msg.id, 'accepted')}
                            className="flex-1 bg-green-50 hover:bg-green-100 text-green-600 font-medium py-1.5 px-3 rounded text-sm flex items-center justify-center gap-1.5 transition-colors border border-green-100 hover:border-green-200 shadow-sm"
                          >
                            <Check className="w-4 h-4" /> Aceitar
                          </button>
                          <button 
                            onClick={() => handleAction(msg.id, 'rejected')}
                            className="flex-1 bg-rose-50 hover:bg-rose-100 text-rose-600 font-medium py-1.5 px-3 rounded text-sm flex items-center justify-center gap-1.5 transition-colors border border-rose-100 hover:border-rose-200 shadow-sm"
                          >
                            <X className="w-4 h-4" /> Recusar
                          </button>
                        </div>
                      )}

                      {msg.status === "accepted" && (
                        <div className="mt-1 flex items-center gap-1.5 text-xs font-semibold text-green-600 bg-green-50 px-2 py-1 rounded w-fit border border-green-100">
                          <Check className="w-3.5 h-3.5" strokeWidth={3} />
                          Pedido Aceito! 🌱
                        </div>
                      )}
                      
                      {msg.status === "rejected" && (
                        <div className="mt-1 flex items-center gap-1.5 text-xs font-semibold text-slate-500 bg-slate-100 px-2 py-1 rounded w-fit border border-slate-200">
                          <X className="w-3.5 h-3.5" strokeWidth={3} />
                          Recusado.
                        </div>
                      )}
                    </div>
                    
                    <div className="text-[11px] text-slate-400 text-right mt-1 ml-4 float-right">
                      {msg.time}
                    </div>
                  </div>
                </div>
              );
            })}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Action Bottom Bar */}
        <div className="bg-slate-50 px-4 py-3 flex items-center gap-3 z-10 relative shadow-[0_-2px_10px_rgba(0,0,0,0.02)]">
          <button 
            onClick={handleNovoTurno}
            className="w-full bg-[#25D366] hover:bg-[#1DA851] text-white font-medium py-3 px-4 rounded-xl shadow-md transition-all flex items-center justify-center gap-2 text-base"
          >
            <FastForward className="w-5 h-5" />
            <span>⏩ Avançar Tempo (Novo Turno)</span>
          </button>
        </div>

        {/* Fake Input Area (Visual Only) */}
        <div className="bg-slate-50 px-4 py-3 flex items-center gap-3 z-10 border-t border-slate-200">
          <Smile className="w-6 h-6 text-slate-500 cursor-not-allowed opacity-50" />
          <Paperclip className="w-6 h-6 text-slate-500 cursor-not-allowed opacity-50" />
          <div className="flex-1 bg-white rounded-lg px-4 py-2.5 text-slate-400 border border-slate-200 text-[15px] cursor-not-allowed opacity-70">
            Você não pode responder, apenas aceitar ou recusar...
          </div>
          <div className="w-10 h-10 rounded-full bg-[#25D366] text-white flex items-center justify-center opacity-50 cursor-not-allowed">
            <Send className="w-5 h-5 ml-1" />
          </div>
        </div>
      </div>
      
    </div>
  );
}
