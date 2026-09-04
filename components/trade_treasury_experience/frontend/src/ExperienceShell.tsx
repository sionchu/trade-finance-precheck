import type { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { ArrowLeftRight, FileCheck2, FileText, Landmark, Sparkles } from "lucide-react";
import { AnimatePresence, motion, MotionConfig } from "motion/react";
import { useEffect, useState, type ComponentType, type ReactElement } from "react";

export type StageId = "deal" | "liquidity" | "treasury" | "review" | "result";
export type ReviewGoal = "overall" | "liquidity" | "fx" | "funding";
export type ResponseAction = "none" | "price" | "receivable" | "credit" | "forward" | "usance";
type StageState = "complete" | "ready" | "blocked";
type Stage = { id: StageId; label: string; state: StageState };
type Choice<T> = { id: T; label: string };
type SnapshotCard = { label: string; value: string; detail: string; status: "neutral" | "success" | "warning" | "danger" };
export type ExperienceData = {
  product: { title: string; subtitle: string }; stages: Stage[]; snapshot: SnapshotCard[];
  insight: { deal: string; company: string; afterCredit: string }; activeStage: StageId;
  reviewGoal: ReviewGoal; responseAction: ResponseAction; reviewGoals: Choice<ReviewGoal>[];
  responseActions: Choice<Exclude<ResponseAction, "none">>[];
  dealFacts: { label: string; value: string; source: string }[];
  reviewState: { ready?: boolean; current?: boolean; loading?: boolean; headline?: string; summary?: string; usedTools?: string[]; error?: string };
};
export type ExperienceState = { active_stage: StageId; review_goal: ReviewGoal; response_action: ResponseAction; primary_action?: "run_review" };
type Tools = Pick<FrontendRendererArgs<ExperienceState, ExperienceData>, "setStateValue" | "setTriggerValue">;
const icons: Record<StageId, ComponentType<{ size?: number; "aria-hidden"?: boolean }>> = { deal: FileText, liquidity: Landmark, treasury: ArrowLeftRight, review: Sparkles, result: FileCheck2 };
const guidance: Record<StageId, string> = {
  deal: "먼저 검토할 거래조건을 확인합니다.",
  liquidity: "거래와 회사의 기존 자금계획을 같은 시점에서 확인합니다.",
  treasury: "무엇을 먼저 확인할까요?",
  review: "현재 근거를 바탕으로 한 번의 거래 검토를 실행합니다.",
  result: "거래 검토 결과",
};

export default function ExperienceShell({ data, setStateValue, setTriggerValue }: Tools & { data: ExperienceData }): ReactElement {
  const [activeStage, setActiveStage] = useState<StageId>(data.activeStage);
  const [reviewGoal, setReviewGoal] = useState<ReviewGoal>(data.reviewGoal);
  const [responseAction, setResponseAction] = useState<ResponseAction>(data.responseAction);
  useEffect(() => setActiveStage(data.activeStage), [data.activeStage]);
  const navigate = (stage: StageId): void => { setActiveStage(stage); setStateValue("active_stage", stage); };
  const selectStage = (stage: Stage): void => { if (stage.state !== "blocked") navigate(stage.id); };
  const runReview = (): void => { navigate("result"); setTriggerValue("primary_action", "run_review"); };
  const chooseResponse = (action: Exclude<ResponseAction, "none">): void => { setResponseAction(action); setStateValue("response_action", action); navigate("treasury"); };
  return <MotionConfig reducedMotion="user" transition={{ duration: 0.2 }}>
    <section className="experience" aria-labelledby="experience-title">
      <header className="hero"><p className="eyebrow">TRADE TREASURY PRE-CHECK</p><h1 id="experience-title">{data.product.title}</h1><p>{data.product.subtitle}</p></header>
      <nav className="stages" aria-label="사전점검 단계">{data.stages.map(stage => { const Icon=icons[stage.id]; const selected=activeStage===stage.id; return <button className={`stage stage--${selected?"active":stage.state}`} type="button" key={stage.id} disabled={stage.state==="blocked"} aria-current={selected?"step":undefined} onClick={()=>selectStage(stage)}><Icon size={19} aria-hidden/><span>{stage.label}</span>{selected&&<motion.span className="stage-indicator" layoutId="stage-indicator"/>}</button>; })}</nav>
      <AnimatePresence mode="wait"><motion.div className="stage-panel" key={activeStage} initial={{opacity:0,y:6}} animate={{opacity:1,y:0}} exit={{opacity:0}}>
        <h2>{guidance[activeStage]}</h2>
        {activeStage==="deal"&&<><div className="fact-grid">{data.dealFacts.map(f=><div key={f.label}><span>{f.label}</span><strong>{f.value}</strong><small>{f.source}</small></div>)}</div><button className="primary-action" type="button" onClick={()=>navigate("liquidity")}>회사 유동성 확인</button></>}
        {activeStage==="liquidity"&&<><div className="insight"><div><span>거래만 본 은행 필요액</span><strong>{data.insight.deal}</strong></div><div><span>회사 자금계획 포함 Peak 부족</span><strong>{data.insight.company}</strong></div><div><span>미사용 한도 적용 후</span><strong>{data.insight.afterCredit}</strong></div></div><p className="support">거래 자체는 한도 내여도 회사의 기존 지급계획을 합치면 같은 시점의 유동성 판단이 달라질 수 있습니다.</p><button className="primary-action" type="button" onClick={()=>navigate("treasury")}>Treasury 검토로 이동</button></>}
        {activeStage==="treasury"&&<><div className="choice-grid">{data.reviewGoals.map(g=><button className={`choice ${reviewGoal===g.id?"choice--selected":""}`} type="button" key={g.id} onClick={()=>{setReviewGoal(g.id);setStateValue("review_goal",g.id)}}>{g.label}</button>)}</div>{responseAction!=="none"&&<p className="support">선택한 대응조건을 아래 결정론적 비교에서 확인합니다.</p>}<button className="primary-action" type="button" onClick={()=>navigate("review")}>거래 검토로 이동</button></>}
        {activeStage==="review"&&<><p className="support">검토에 사용할 근거: 거래 분석 · Stress / 조건 경계 · 회사 유동성 / Treasury · 공식 결제 Context</p><button className="primary-action" type="button" disabled={!data.reviewState.ready} onClick={runReview}>이 조건으로 거래 검토</button></>}
        {activeStage==="result"&&<>{data.reviewState.loading?<p className="support">현재 거래 근거를 확인하고 있습니다.</p>:data.reviewState.error?<p className="error">{data.reviewState.error}</p>:data.reviewState.current?<motion.div initial={{opacity:0}} animate={{opacity:1}}><h3>{data.reviewState.headline}</h3><p>{data.reviewState.summary}</p>{data.reviewState.usedTools?.length?<p className="support">확인 완료 · {data.reviewState.usedTools.join(" · ")}</p>:null}<h3>어떤 조건을 바꿔볼까요?</h3><div className="choice-grid">{data.responseActions.map(a=><button className="choice" type="button" key={a.id} onClick={()=>chooseResponse(a.id)}>{a.label}</button>)}</div></motion.div>:<p className="support">조건이 변경되어 다시 검토가 필요합니다.</p>}</>}
      </motion.div></AnimatePresence>
      <div className="snapshot-grid">{data.snapshot.map(card=><motion.article className={`snapshot-card snapshot-card--${card.status}`} key={card.label} whileHover={{y:-2}}><span>{card.label}</span><strong>{card.value}</strong><small>{card.detail}</small></motion.article>)}</div>
    </section>
  </MotionConfig>;
}
